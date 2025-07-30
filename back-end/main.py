from dotenv import load_dotenv
import os
import pandas as pd
import time

from config import constants
from core import RouteFetcher
from model import BusSenseAssistant

#TODO:
# [ ] - Verificar resultados do modelo e melhora-los
# [ ] - Adicionar os itens restantes no logs/user_interactions.csv pelo script

if __name__ == "__main__":
    load_dotenv()
    url = constants.REST_API_URL + "/bus-route"
    get_routes = RouteFetcher(url)
    routes_df = get_routes.fetch_routes()

    assistant = BusSenseAssistant(routes_data_path=constants.DATA_FILE_PATH + 'llm_generated_routes.csv')
    assistant.start()
