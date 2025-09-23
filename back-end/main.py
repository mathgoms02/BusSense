from dotenv import load_dotenv

from config import constants
from core import RouteFetcher
from AI.model import BusSenseAssistant
from AI.model import metrics

#TODO:
# [ ] - Verificar resultados do modelo e melhora-los
# [ ] - Adicionar os itens restantes no logs/user_interactions.csv pelo script
# [ ] - Melhorar o output de audio

if __name__ == "__main__":
    load_dotenv()
    url = constants.REST_API_URL + "/bus-route"
    get_routes = RouteFetcher(url)
    routes_df = get_routes.fetch_routes()

    # assistant = BusSenseAssistant(routes_data_path=constants.DATA_FILE_PATH + 'llm_generated_routes.csv')
    # assistant.start()

    # metric = metrics.ModelEvaluator("/home/matheusg/Documents/UNASP/BusSense/back-end/data/db_metrics.csv")
    metric = metrics.ModelEvaluator("/home/matheusg/Documents/UNASP/BusSense/back-end/data/model_test_data_clean_utf8.csv")

    metric.run_full_evaluation()