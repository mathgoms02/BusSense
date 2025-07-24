import pandas as pd
import requests
import re
import json

from audio.audio_capture import AudioCapture
from audio.text_to_speach import TextTSpeech
from model.agents.agent_feedback_classifier import FeedbackClassifierAgent
from config import constants
from utils.route_embeddings import RouteEmbeddings
from utils.logger import InteractionLogger

#TODO:
# - [ ] Refatorar para usar uma máquina de estados
# - [ ] Melhorar a lógica de feedback (retornar um "OK" ou "Obrigado" para o usuário)
# - [ ] Estudar melhor ideia do Llama
# - [ ] Mesclar script com o LlamaThinking

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

        # --- Componentes para interagir com o LLM (da sua classe Llama) ---
        self.llm_url = constants.LLAMA_API_URL

        # --- MÁQUINA DE ESTADOS ---
        self.state = "AGUARDANDO_ROTA"
        self.last_interaction_id = None
        print(f"Estado inicial: {self.state}")


    def start(self):
            """ Inicia o loop de escuta do assistente. """
            print("\nAssistente pronto. Clique na tela (simulado) para falar.")
            while True:
                # Esta chamada simula o usuário tocando na tela e falando.
                # Em um app real, isso seria um evento de clique.
                transcribed_text = self.recorder.listen()

                if transcribed_text:
                    self.handle_user_input(transcribed_text)


    def handle_user_input(self, text: str):
        """ Ponto de entrada central que decide o que fazer com base no estado. """
        print(f"\n--- Processando Input no Estado: {self.state} ---")

        if self.state == "AGUARDANDO_ROTA":
            # Se estamos esperando uma rota, processamos o texto como uma nova solicitação.
            self._process_new_route_request(text)

        #TODO: Adicionar modelo para verificar se o input é feedback 9FEITO
        elif self.state == "AGUARDANDO_FEEDBACK":
            # Se acabamos de dar uma rota, o input é provavelmente um feedback.
            self._process_potential_feedback(text)


    def _process_new_route_request(self, text: str):
        """ Lógica para lidar com uma nova solicitação de rota. """
        # (Esta é a lógica principal da sua antiga classe LlamaThinking)
        print("Interpretando como uma nova solicitação de rota...")
        log_data = {'user_query': text}

        # Extrai locais, busca embedding, gera prompt, etc.
        # ... (código de extração e busca) ...
        locations = self._extract_location_from_text(text)
        filtered_data, _ = self.route_searcher.search(locations['origin'], locations['destination'])
        prompt = self._generate_route_prompt(filtered_data)

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

        # *** MUDANÇA DE ESTADO CRUCIAL ***
        self.state = "AGUARDANDO_FEEDBACK"
        print(f"Estado alterado para: {self.state}. Aguardando feedback para a interação {self.last_interaction_id}.")


    def create_message(self, message, role):
            return {"role": role,
                "content": message}


    def _process_potential_feedback(self, text: str):
        """ Lógica para lidar com um input que pode ser feedback. """
        print("Interpretando como potencial feedback...")

        # Usa o agente classificador para entender a intenção
        intent = self.feedback_classifier._classify_intent(text) # Usando o método interno que já criamos
        print(f"Intenção detectada: {intent}")

        if intent == "nova_solicitacao":
            # O usuário ignorou o contexto de feedback e fez uma nova pergunta.
            print("O usuário fez uma nova solicitação. Resetando o estado.")
            self.state = "AGUARDANDO_ROTA"
            self.handle_user_input(text) # Processa o mesmo texto novamente, mas no novo estado.
        else:
            # É um feedback! Processa e volta ao estado inicial.
            if self.last_interaction_id:
                self.feedback_classifier._handle_intent(self.last_interaction_id, intent, text)

            # *** MUDANÇA DE ESTADO CRUCIAL ***
            self.state = "AGUARDANDO_ROTA"
            print(f"Feedback processado. Estado alterado para: {self.state}.")

    # --- Métodos de Suporte (extraídos da sua classe Llama) ---
    def _extract_location_from_text(self, text):
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

    # def fetch_routes(url: str) -> pd.DataFrame:
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         data = response.json()
    #         df = pd.DataFrame(data)
    #         df = df[['route_short_name', 'route_name_start', 'route_name_end']]
    #         df.columns = ['RouteCode', 'RouteStart', 'RouteEnd']
    #         return df
    #     else:
    #         raise Exception(f"API Error: {response.status_code}")

# --- Para executar o programa ---
if __name__ == "__main__":
    assistant = BusSenseAssistant(routes_data_path=constants.DATA_FILE_PATH + 'llm_generated_routes.csv')
    assistant.start()