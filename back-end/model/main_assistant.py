import json
import pandas as pd
import re

from audio import TextTSpeech, AudioCapture
from config import constants
from model.agents import FeedbackClassifierAgent
from model.client import LlamaClient
from model.states.base_state import State
from model.states.anfitriao_state import AnfitriaoState
from utils import RouteEmbeddings, InteractionLogger
from model.intent_svm import IntentSVM  # novo


class BusSenseAssistant:
    def __init__(self, routes_data_path: str):
        # --- Carrega todos os componentes na inicialização ---
        print("Iniciando o BusSense Assistant...")
        routes_df = pd.read_csv(routes_data_path)
        self.recorder = AudioCapture()
        self.tts = TextTSpeech("")
        self.intent_svm = IntentSVM(model_path="/home/matheusg/Documents/UNASP/BusSense/back-end/model/intent_svm.pkl", threshold=0.9)
        self.logger = InteractionLogger()
        self.route_searcher = RouteEmbeddings(routes_df)
        self.feedback_classifier = FeedbackClassifierAgent()
        self.llm_url = constants.LLAMA_API_URL
        self.last_interaction_id = None
        self.llm_client = LlamaClient(api_url=constants.LLAMA_API_URL, model_name=constants.LLAMA_MODEL_NAME)
        self.state = AnfitriaoState(self)   # Maquina de Estado

        print(f"Estado inicial: {self.state.__class__.__name__}")


    def transition_to(self, new_state: State):
        """ Método central para mudar de estado."""
        self.state = new_state
        print(f"Transição para o novo estado: {self.state.__class__.__name__}")


    def start(self):
            """ Inicia o loop de escuta do assistente. """
            print("\nAssistente pronto. Clique na tela (simulado) para falar.")
            while True:
                # Simulando toque do usuário na tela para iniciar a interação
                transcribed_text = self.recorder.listen()
                transcribed_text = "Sou de São Paulo, quero ir para Campinas"

                print(f"[DEBUG]: Rota solicitada: {transcribed_text}")

                if transcribed_text:
                    self.state.handle_user_input(transcribed_text)


    def _extract_location_from_text(self, text):
        """ Extrai a origem e o destino de uma frase do usuário usando o modelo Llama. """

        system_prompt = (
            "Você é um assistente que extrai a cidade de origem e destino da frase de um usuário. "
            "Retorne APENAS um objeto JSON válido no seguinte formato:\n"
            '{ "origin": "CITY1", "destination": "CITY2" }\n'
            "Se não conseguir encontrar, retorne:\n"
            '{ "origin": "UNKNOWN", "destination": "UNKNOWN" }\n'
            "Não escreva mais nada. Não conte histórias. Não explique."
        )

        response_text = self.llm_client.chat_completion(system_prompt=system_prompt,
                                                        user_prompt=text,
                                                        temperature=0.2,
                                                        max_tokens=100)

        try:
            clean_text = re.sub(r"```(?:json)?", "", response_text).strip()
            print("[DEBUG] Raw result:", clean_text)
            return json.loads(clean_text)
        except Exception as e:
            print("Erro ao extrair locais:", e)
            return {"origin": "UNKNOWN", "destination": "UNKNOWN"}


    def _generate_route_prompt(self, filtered_data):
        """ Gera o prompt para o modelo Llama com as rotas filtradas """

        if filtered_data.empty:
            filtered_data = self.routes_data.head(5)

        json_data = filtered_data.to_json(orient='records')

        prompt = f"""
            Você é um assistente especialista em transporte público. Com base nas seguintes rotas de ônibus em formato JSON,
            sugira a melhor rota para o usuário. Sua tarefa é identificar a melhor rota e responder com uma frase concisa.
            Use 'Linha' para o RouteCode, 'Ponto Inicial' para RouteStart, e 'Ponto Final' para RouteEnd.
            Por exemplo:
            ('origin': 'Monte Mor', 'destination': 'Campinas') A melhor rota é a Linha 708, que vai de Monte Mor até Campinas.
            Não inclua acentos graves (`) ou explicações adicionais. Retorne apenas a frase final.

            {json_data}
        """
        return prompt


    def _classify_intent_with_llm(self, text: str) -> str:
        """
        Usa o LLM para classificar a intenção do Usuário.
        Retorna uma string simples: 'solicitar_rota', 'feedback', 'conversa_geral' ou 'desconhecido'.
        """
        system_prompt = (
            "Sua tarefa é classificar a intenção de uma frase do usuário para um assistente de transporte público. "
            "Responda APENAS com uma das seguintes palavras: "
            "Siga os exemplos abaixo:\n\n"
            "Usuário: 'Olá, tudo bem?'\n"
            "Assistente: conversacao_geral\n\n"
            "Usuário: 'Qual o ônibus para o centro?'\n"
            "Assistente: solicitar_rota\n\n"
            "Usuário: 'Gostei muito do serviço, obrigado!'\n"
            "Assistente: feedback\n\n"
            "Usuário: 'O motorista não parou para mim.'\n"
            "Assistente: feedback\n\n"
            "Usuário: 'como eu chego na prefeitura?'\n"
            "Assistente: solicitar_rota\n\n"
            "Usuário: 'valeu'\n"
            "Assistente: conversacao_geral\n\n"
            "Agora, classifique a seguinte frase do usuário. Não escreva mais nada. Apenas a palavra de classificação."
        )

        try:
            # reutilizar a função _call_llm, mas talvez com parametros dieferentes no futuro
            response = self.llm_client.chat_completion(system_prompt=system_prompt,
                                                       user_prompt=text,
                                                       temperature=0.1,
                                                       max_tokens=10)

            cleaned_response = response.strip().lower().replace("'", "")
            if cleaned_response in ['solicitar_rota', 'feedback', 'conversacao_geral']:
                print(f"[DEBUG] Intenção classificada: {cleaned_response}")
                return cleaned_response
            else:
                print(f"RAW Response: '{response}'")
                return 'desconhecido'
        except Exception as e:
            print(f"[ERROR] Erro ao classificar intenção: {e}")
            return 'desconhecido'
