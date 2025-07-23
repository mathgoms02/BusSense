import os
import pandas as pd
import requests
from dotenv import load_dotenv
from model.gemini_analysis import GeminiThinking
from model.llama_analysis import LlamaThinking
import time

def fetch_routes(url: str) -> pd.DataFrame:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df = df[['route_short_name', 'route_name_start', 'route_name_end']]
        df.columns = ['RouteCode', 'RouteStart', 'RouteEnd']
        return df
    else:
        raise Exception(f"API Error: {response.status_code}")

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    url = "http://localhost:8000/api/bus-route"
    routes_df = fetch_routes(url)

    while True:
        # assistant_choose = input(
        #     "Choose the model:\n"
        #     "  1 - Gemini\n"
        #     "  2 - Llama\n"
        #     "Enter your choice (1 or 2): "
        # )

        assistant_choose = "2"

        if assistant_choose == "1":
            print('gemini')
            assistant = GeminiThinking(api_key=api_key, routes_data=routes_df)
        elif assistant_choose == "2":
            assistant = LlamaThinking(routes_data=routes_df)
            print('llama')
        else:
            print("\nEscolhe 1 ou 2 seu cabaço")
            time.sleep(2)
            os.system("clear")
            continue
        assistant.run()
        break
