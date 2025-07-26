import pandas as pd
import requests
import re
import json

from audio import TextTSpeech, AudioCapture
from model.agents import FeedbackClassifierAgent
from config import constants
from utils import RouteEmbeddings, InteractionLogger

#TODO:
# - [ ] Refatorar para usar uma máquina de estados
# - [X] Melhorar a lógica de feedback (retornar um "OK" ou "Obrigado" para o usuário)
# - [ ] Estudar melhor ideia do Llama
# - [ ] Mesclar script com o LlamaThinking
# - [ ] Criar Client para o Assistente para tools

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

        # Interagindo com o modelo Llama via Requests
        self.llm_url = constants.LLAMA_API_URL

        # --- MÁQUINA DE ESTADOS ---
        #TODO:  Adicionar um self.state inicial para controlar o fluxo
        #       Estado esse que vai separar se é uma interação normal com o usuário, se é uma solicitação de rota ou se é um feedback.
        self.state = "AGUARDANDO_ROTA"
        self.last_interaction_id = None
        print(f"Estado inicial: {self.state}")


    def start(self):
            """ Inicia o loop de escuta do assistente. """
            print("\nAssistente pronto. Clique na tela (simulado) para falar.")
            while True:
                # Simulando toque do usuário na tela para iniciar a interação
                transcribed_text = self.recorder.listen()

                if transcribed_text:
                    self.handle_user_input(transcribed_text)


    def handle_user_input(self, text: str):
        """ Ponto de entrada central que decide o que fazer com base no estado. """
        print(f"\n--- Processando Input no Estado: {self.state} ---")

        #TODO: Adicionar modelo genérico de acordo com o self.state primário ou "Anfitrião"
        if self.state == "AGUARDANDO_ROTA":
            self._process_new_route_request(text)

        elif self.state == "AGUARDANDO_FEEDBACK":
            # Se acabamos de dar uma rota, o input é provavelmente um feedback.
            self._process_potential_feedback(text)


    def _process_new_route_request(self, text: str):
        """ Lógica para lidar com uma nova solicitação de rota. """
        print("Interpretando como uma nova solicitação de rota...")
        log_data = {'user_query': text}

        # Extrai origin e destination pela query
        locations = self._extract_location_from_text(text)
        # Filtra no banco pela origin e destination
        filtered_data, _ = self.route_searcher.search(locations['origin'], locations['destination'])
        # Gera o prompt para o modelo Llama
        prompt = self._generate_route_prompt(filtered_data)

        # Padroniza as mensagens para o LLM
        system_message = self.create_message(prompt, 'system')
        user_message = self.create_message(text, 'user')

        # Obtém a resposta do LLM
        response_text = self._call_llm(system_message, user_message)
        print("Resposta do Assistente:", response_text)
        self.tts.text = response_text
        self.tts.convert_to_speech()

        # Loga a interação
        log_data['assistant_response'] = response_text
        self.last_interaction_id = self.logger.log(log_data)

        #TODO: Voltar para estado anfitrião
        # *** MUDANÇA DE ESTADO "CRUCIAL" ***
        self.state = "AGUARDANDO_FEEDBACK"
        print(f"Estado alterado para: {self.state}. Aguardando feedback para a interação {self.last_interaction_id}.")


    def create_message(self, message, role):
            return {"role": role,
                "content": message}


    def _process_potential_feedback(self, text: str):
        """ Lógica para lidar com um input que pode ser feedback. """
        print("Interpretando como potencial feedback...")

        # Usa o agente classificador para entender a intenção
        intent = self.feedback_classifier._classify_intent(text) # Classifica por palavras-chave
        print(f"Intenção detectada: {intent}")

        if intent == "nova_solicitacao":
            # O usuário ignorou o contexto de feedback e fez uma nova pergunta.
            print("O usuário fez uma nova solicitação. Resetando o estado.")
            self.state = "AGUARDANDO_ROTA"
            self.handle_user_input(text)
        else:
            # É um feedback! Processa e volta ao estado inicial.
            if self.last_interaction_id:
                self.feedback_classifier._handle_intent(self.last_interaction_id, intent, text)

            #TODO: Voltar para estado anfitrião
            # *** MUDANÇA DE ESTADO "CRUCIAL" ***
            self.state = "AGUARDANDO_ROTA"
            self.tts.text = f"Feedback processado."
            self.tts.convert_to_speech()
            print(f"Feedback processado. Estado alterado para: {self.state}.")


    def _extract_location_from_text(self, text):
        """ Extrai a origem e o destino de uma frase do usuário usando o modelo Llama. """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an assistant that extracts the city of origin and destination from a user's sentence. "
                    "Return ONLY a valid JSON object in the following format:\n"
                    '{ "origin": "CITY1", "destination": "CITY2" }\n'
                    "If you can't find one, return:\n"
                    '{ "origin": "UNKNOWN", "destination": "UNKNOWN" }\n'
                    "Do not write anything else. Do not tell stories. Do not explain."
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
            You are an expert public transport assistant. Based on the following bus routes in JSON format,
            suggest the best one to the user. Your task is to identify the best route and respond with a concise sentence.
            Use 'Linha' for the RouteCode, 'Ponto Inicial' for RouteStart, and 'Ponto Final' for RouteEnd.
            For example: "A melhor rota é a Linha 708, que vai de Monte Mor até Campinas."
            Do not include any backticks or additional explanations. Only return the final sentence.

            {json_data}
        """
        return prompt


    def _call_llm(self, prompt, user_text):
        """ Faz a chamada ao modelo Llama (via requests) com o prompt e o texto do usuário. """
        form = {
            "model": constants.LLAMA_MODEL_NAME,
            "temperature": 0.7,
            "max_tokens": 2048,
            "seed": 42,
            "messages": [prompt, user_text],
            "repeat_last_n": 64,
            "repeat_penalty": 1.2
        }

        response = requests.post(self.llm_url, json=form)
        json_list = response.json()

        if 'error' in json_list:
            print("Erro na requisição:", json_list['error']['message'])
            return "Desculpe, não consegui entender a solicitação. Tente novamente com menos detalhes."

        return json_list['choices'][0]['message']['content']


if __name__ == "__main__":
    assistant = BusSenseAssistant(routes_data_path=constants.DATA_FILE_PATH + 'llm_generated_routes.csv')
    assistant.start()
