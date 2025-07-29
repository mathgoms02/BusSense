import pandas as pd
import requests
import re
import json

from audio import TextTSpeech, AudioCapture
from model.agents import FeedbackClassifierAgent
from config import constants
from utils import RouteEmbeddings, InteractionLogger

#TODO:
# - [X] Refatorar para usar uma máquina de estados
# - [X] Criar um Anfitrião (AnfitriaoState) que vai classificar a intenção do usuário
# - [X] Melhorar a lógica de feedback (retornar um "OK" ou "Obrigado" para o usuário)
# - [ ] Refatorar todo projeto, eliminando agentes e scripts desnecessários
# - [ ] Criar Client para o Assistente para tools

class State:
    """ Classe base para estados do assistente. """
    def __init__(self, assistant):
        self.assistant = assistant

    def handle_user_input(self, text: str):
        """ Método que será implementado por cada estado para lidar com o input. """
        raise NotImplementedError("Subclasses must implement this method.")


class AnfitriaoState(State):
    """
    O estado central (Anfitrião). Ele é responsável por classificar
    a intenção do usuário e decidir para qual estado ir.
    """

    def handle_user_input(self, text: str):
        print("[AnfitriaoState]: Classificando intenção...")

        intent = self.assistant._classify_intent_with_llm(text)
        print(f"[AnfitriaoState]: Intenção classificada como: {intent}")

        if intent == 'solicitar_rota':
            print("[AnfitriaoState]: Intenção 'solicitar_rota' detectada. Transicionando.")
            self.assistant.transition_to(RouteState(self.assistant))
            self.assistant.state.handle_user_input(text)

        elif intent == 'feedback':
            print("[AnfitriaoState]: Intenção 'feedback' detectada. Transicionando.")
            self.assistant.transition_to(FeedbackState(self.assistant))
            self.assistant.state.handle_user_input(text)

        elif intent == 'conversacao_geral':
            print("[AnfitriaoState]: Intenção 'conversacao_geral' detectada.")

            system_prompt = (
                "Você é 'BusSense', um assistente de IA focado em transporte público. Sua personalidade é útil e profissional."
                "Siga estas regras RIGOROSAMENTE:\n"
                "1. Responda de forma direta e objetiva.\n"
                "2. Mantenha as respostas curtas, com no máximo duas frases.\n"
                "3. NUNCA use emojis, emoticons ou gírias.\n"
                "4. NUNCA faça perguntas pessoais como 'Tudo bem com você?'.\n\n"
                "Exemplo de resposta ideal para a entrada 'Olá':\n"
                "Olá! Sou o BusSense, seu assistente de transporte. Como posso ajudar com sua rota hoje?"
            )

            messages = [
                self.assistant.create_message(system_prompt, 'system'),
                self.assistant.create_message(text, 'user')
            ]

            response = self.assistant._call_llm(messages, temperature=0.4, max_tokens=60)
            print("Resposta do Assistente:", response)
            self.assistant.tts.text = response
            self.assistant.tts.convert_to_speech()

        else: # intent == 'desconhecido'
            print("[AnfitriaoState]: Não foi possível determinar a intenção.")
            response = "Desculpe, não entendi. Pode repetir?"
            print("Resposta do Assistente:", response)
            self.assistant.tts.text = response
            self.assistant.tts.convert_to_speech()


class RouteState(State):
    """ Estado para processar uma solicitação de rota. """
    def handle_user_input(self, text: str):
        print("[RouteState]: Processando solicitação de rota...")
        log_data = {'user_query': text}

        # Extrai origin e destination pela query
        locations = self.assistant._extract_location_from_text(text)
        # Filtra no banco pela origin e destination
        filtered_data, _ = self.assistant.route_searcher.search(locations['origin'], locations['destination'])
        # Gera o prompt para o modelo Llama
        prompt = self.assistant._generate_route_prompt(filtered_data)

        # Padroniza as mensagens para o LLM
        messages = [
            self.assistant.create_message(prompt, 'system'),
            self.assistant.create_message(text, 'user')
        ]
        # Obtém a resposta do LLM
        response_text = self.assistant._call_llm(messages)
        print("Resposta do Assistente:", response_text)

        self.assistant.tts.text = response_text
        self.assistant.tts.convert_to_speech()

        log_data['assistant_response'] = response_text
        self.assistant.last_interaction_id = self.assistant.logger.log(log_data)

        print("[RouteState]: Mudando para estado Anfitrião.")
        self.assistant.transition_to(AnfitriaoState(self.assistant))


class FeedbackState(State):
    """ Estado para aguardar e processar o feedback do usuário."""
    def handle_user_input(self, text: str):
        print("[FeedbackState]: Processando feedback...")

        # Usa o agente classificador para entender a intenção
        intent_subtype = self.assistant.feedback_classifier._classify_intent(text)
        print(f"Intenção detectada: {intent_subtype}")

        if self.assistant.last_interaction_id:
            self.assistant.feedback_classifier._handle_intent(self.assistant.last_interaction_id, intent_subtype, text)
        else:
            print("Registrando feedback geral do usuário.")
            self.assistant.logger.log({'user_feedback_geral': text})

        response = "Obrigado pelo seu feedback!"
        print("Resposta do Assistente:", response)
        self.assistant.tts.text = response
        self.assistant.tts.convert_to_speech()

        print("[FeedbackState]: Retornando ao estado anfitrião.")
        self.assistant.transition_to(AnfitriaoState(self.assistant))

# --- FIM DA MÁQUINA DE ESTADOS ---

class BusSenseAssistant:
    def __init__(self, routes_data_path: str):
        # --- Carrega todos os componentes na inicialização ---
        print("Iniciando o BusSense Assistant...")
        routes_df = pd.read_csv(routes_data_path)
        self.recorder = AudioCapture()
        self.tts = TextTSpeech("")
        self.logger = InteractionLogger()
        self.route_searcher = RouteEmbeddings(routes_df)
        self.feedback_classifier = FeedbackClassifierAgent()
        self.llm_url = constants.LLAMA_API_URL
        self.last_interaction_id = None

        # --- MÁQUINA DE ESTADOS ---
        self.state = AnfitriaoState(self)
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

                if transcribed_text:
                    self.state.handle_user_input(transcribed_text)

    def _extract_location_from_text(self, text):
        """ Extrai a origem e o destino de uma frase do usuário usando o modelo Llama. """
        messages = [
            {
                "role": "system",
                "content": (
                    "Você é um assistente que extrai a cidade de origem e destino da frase de um usuário. "
                    "Retorne APENAS um objeto JSON válido no seguinte formato:\n"
                    '{ "origin": "CITY1", "destination": "CITY2" }\n'
                    "Se não conseguir encontrar, retorne:\n"
                    '{ "origin": "UNKNOWN", "destination": "UNKNOWN" }\n'
                    "Não escreva mais nada. Não conte histórias. Não explique."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ]

        response = requests.post(self.llm_url, json={
            "model": constants.LLAMA_MODEL_NAME,
            "temperature": 0.3,
            "max_tokens": 100,
            "messages": messages,
        })

        try:
            result_text = response.json()['choices'][0]['message']['content']
            clean_text = re.sub(r"```(?:json)?", "", result_text).strip()
            print("[DEBUG] Raw result:", clean_text)
            locations = json.loads(clean_text)
        except Exception as e:
            print("Erro ao extrair locais:", e)
            locations = {"origin": "UNKNOWN", "destination": "UNKNOWN"}

        return locations

    def _generate_route_prompt(self, filtered_data):
        """ Gera o prompt para o modelo Llama com as rotas filtradas """

        if filtered_data.empty:
            filtered_data = self.routes_data.head(5)

        json_data = filtered_data.to_json(orient='records')

        prompt = f"""
            Você é um assistente especialista em transporte público. Com base nas seguintes rotas de ônibus em formato JSON, 
            sugira a melhor rota para o usuário. Sua tarefa é identificar a melhor rota e responder com uma frase concisa.
            Use 'Linha' para o RouteCode, 'Ponto Inicial' para RouteStart, e 'Ponto Final' para RouteEnd.
            Por exemplo: "A melhor rota é a Linha 708, que vai de Monte Mor até Campinas."
            Não inclua acentos graves (`) ou explicações adicionais. Retorne apenas a frase final.

            {json_data}
        """
        return prompt

    def _call_llm(self, messages: list, temperature: float = 0.7, max_tokens: int = 2048):
        """ Faz a chamada ao modelo Llama (via requests) com o prompt e o texto do usuário. """
        form = {
            "model": constants.LLAMA_MODEL_NAME,
            "temperature": temperature, # Quanto maior a temperatura, mais criativa a resposta (Ruim para classificação)
            "max_tokens": max_tokens,
            "seed": 42,
            "messages": messages,
            "repeat_last_n": 64,
            "repeat_penalty": 1.2
        }
        try:
            response = requests.post(self.llm_url, json=form)
            json_list = response.json()

            if 'error' in json_list:
                print("Erro na requisição:", json_list['error']['message'])
                return "Desculpe, não consegui entender a solicitação. Tente novamente com menos detalhes."
            print("[DEBUG] Resposta do LLM:", json_list['choices'][0]['message']['content'])
            return json_list['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Erro ao chamar o LLM: {e}")
            return "Desculpe, estou com problemas para me conectar ao meu cérebro. Tente novamente mais tarde."

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

        messages = [
            self.create_message(system_prompt, 'system'),
            self.create_message(text, 'user')
        ]

        try:
            # reutilizar a função _call_llm, mas talvez com parametros dieferentes no futuro
            response = self._call_llm(messages, temperature=0.1, max_tokens=10)

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

    def create_message(self, message, role):
            return {"role": role,
                "content": message}


if __name__ == "__main__":
    assistant = BusSenseAssistant(routes_data_path=constants.DATA_FILE_PATH + 'llm_generated_routes.csv')
    assistant.start()
