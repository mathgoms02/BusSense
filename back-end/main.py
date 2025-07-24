import os
import pandas as pd
from dotenv import load_dotenv
from config import constants
from core.routes import RouteFetcher
from model.gemini_analysis import GeminiThinking
from model.llama_analysis import LlamaThinking
import time


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    url = constants.REST_API_URL + "/bus-route"
    get_routes = RouteFetcher(url)
    routes_df = get_routes.fetch_routes()

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
            print("\nEscolha apenas 1 ou 2.\n")
            time.sleep(1)
            os.system("clear")
            continue
        assistant.run()
        break
