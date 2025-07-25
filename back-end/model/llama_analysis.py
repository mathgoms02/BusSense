import json
import pandas as pd
import re
import requests
import unicodedata

from audio import AudioCapture, TextTSpeech
from config import constants
from utils import RouteEmbeddings, InteractionLogger
from model.agents import FeedbackClassifierAgent

class LlamaThinking:
    def __init__(self, routes_data: pd.DataFrame):
        self.recorder = AudioCapture()
        self.routes_data = routes_data
        self.tts = TextTSpeech("")
        self.url = constants.LLAMA_API_URL

        # Otimização: Inicializando o buscador e o Logger aqui
        self.route_search = RouteEmbeddings(self.routes_data)
        self.logger = InteractionLogger()
        self.feedback_classifier = FeedbackClassifierAgent()


    def create_message(self, message, role):
        return {"role": role,
            "content": message}


    def normalize(self, text):
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8').lower()


    def generate_prompt(self, filtered_data: pd.DataFrame):
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



    def extract_location_from_text(self, user_text):
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
                "content": user_text
            }
        ]

        response = requests.post(self.url, json={
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




    def route_requisition_llama(self, system_message, user_message):
        form = {
            "model": constants.LLAMA_MODEL_NAME,
            "temperature": 0.7,
            "max_tokens": 2048,
            "seed": 42,
            "messages": [system_message, user_message],
            "repeat_last_n": 64,
            "repeat_penalty": 1.2
        }

        response = requests.post(self.url, json=form)
        json_list = response.json()

        if 'error' in json_list:
            print("Erro na requisição:", json_list['error']['message'])
            return "Desculpe, não consegui entender a solicitação. Tente novamente com menos detalhes."

        return json_list['choices'][0]['message']['content']



    def run(self):
        # user_query = self.recorder.listen()
        # user_query = "Sou do Jardim Amanda e quero ir para Campinas"
        user_query = "Sou de Monte Mor e quero ir para Campinas"

        if not user_query:
            print("Nenhum audio detectado,")
            self.tts.text = "Nenhum audio detectado, tente novamente."
            self.tts.convert_to_speech()
            raise Exception

        log_data = {'user_query': user_query}

        locations = self.extract_location_from_text(user_query)
        log_data['extracted_origin'] = locations.get('origin')
        log_data['extracted_destination'] = locations.get('destination')

        filtered_data, distances = self.route_search.search(
            locations['origin'], locations['destination'], top_k=1
        )

        prompt = self.generate_prompt(filtered_data)
        system_message = self.create_message(prompt, 'system')
        user_message = self.create_message(user_query, 'user')

        response_text = self.route_requisition_llama(system_message, user_message)

        log_data['assistant_response'] = response_text

        print(response_text)

        # responder
        self.tts.text = response_text
        self.tts.convert_to_speech()
        interaction_id = self.logger.log(log_data)

        print("Aguardando feedback do usuário...")
        feedback_prompt_text = "A informação foi útil? Você pode me dar um feedback ou fazer outra pergunta"
        self.tts.text = feedback_prompt_text
        self.tts.convert_to_speech()

        feedback_text = self.recorder.listen()
        if feedback_text and interaction_id:
            # passa o texto para o agente classificador
            self.feedback_classifier.process_feedback_text(interaction_id, feedback_text)
        else:
            print("Nenhum feedback fornecido ou interação ID não encontrado.")

        # self.tts = TextTSpeech(response_text)
        # self.tts.convert_to_speech()
