import json
import os
import pandas as pd
import re
import requests
import unicodedata

class LlamaAgents:
    def __init__(self, routes_data: pd.DataFrame):
        self.url = 'http://127.0.0.1:8080/v1/chat/completions'
        self.prompt = f"""
        Você é um gerador de frases naturais para simular pessoas perguntando como ir de um local para outro.

        Você receberá uma Origem e um Destino. Gere apenas uma frase, como se uma pessoa estivesse perguntando informalmente como chegar no destino a partir da origem.

        Regras:
        - Seja direto e fale como uma pessoa comum.
        - Varie a estrutura e o estilo das frases.
        - NÃO inverta origem e destino.
        - NÃO invente nomes de lugares que não estão no input.
        - NÃO inclua explicações.
        - Retorne apenas a frase, sem “Input”, “Output” ou quebra de linha.

        Exemplos:

        Origem: Hortolândia
        Destino: Campinas
        Frase: Tô em Hortolândia e queria saber como faço pra chegar em Campinas.

        Origem: Metrô Tatuapé
        Destino: Parque Ibirapuera
        Frase: Como eu vou do Metrô Tatuapé até o Parque Ibirapuera?

        Origem: Osasco
        Destino: Metrô Armênia
        Frase: Preciso sair de Osasco e chegar no Metrô Armênia. Como eu faço?

        """


    def create_message(self, message, role):
        return {"role": role,
            "content": message}

    def normalize(self, text):
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8').lower()



    def make_phrase(self, user_text):
        messages = [
            {
                "role": "system",
                "content": (
                    self.prompt
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ]

        response = requests.post(self.url, json={
            "model": "ggml-org_gemma-3-1b-it-GGUF_gemma-3-1b-it-Q4_K_M.gguf",
            "temperature": 0.8,
            "max_tokens": 100,
            "messages": messages,
        })

        try:
            result_text = response.json()['choices'][0]['message']['content']
            result_text = self.normalize(result_text)
        except Exception as e:
            print("Erro ao JSON:", e)

        return result_text
