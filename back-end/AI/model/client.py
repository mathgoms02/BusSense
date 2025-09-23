import requests
import json


class LlamaClient:
    """ Cliente responsável por gerenciar todas as interações com a API do Llama """
    def __init__(self, api_url: str, model_name: str):
        self.api_url = api_url
        self.model_name = model_name


    def _create_message(self, message, role):
            return {"role": role,
                "content": message}


    def chat_completion(self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 2048):
        """ Método central para enviar a requisição para API """
        messages = [
             self._create_message(system_prompt, 'system'),
             self._create_message(user_prompt, 'user')
        ]

        form = {
            "model": self.model_name,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "seed": 42,
            "messages": messages,
            "repeat_last_n": 64,
            "repeat_penalty": 1.2
        }
        try:
            response = requests.post(self.api_url, json=form)
            response.raise_for_status()     # Lança um erro para respostas 4xx/5xx
            json_response = response.json()

            if 'error' in json_response:
                print(f"Erro na API: {json_response['error']['message']}")
                return "Desculpe, ocorreu um erro na comunicação"

            response_content = json_response['choices'][0]['message']['content']
            return response_content
        except requests.exceptions.RequestException as e:
            return "Desculpe, estou com problemas para me conectar ao meu cérebro."
        except json.JSONDecodeError:
            return "Ocorreu um erro inesperado ao processar a resposta."
