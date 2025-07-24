from smart_agents.agent_db_generator import LlamaAgents
import pandas as pd
import requests
from config import constants

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
    url = constants.REST_API_URL + "/bus-route"
    routes_df = fetch_routes(url)

    agent = LlamaAgents(routes_data=routes_df)

    routes_df['llm_generated'] = ""

    i = 0
    size = len(routes_df)
    all_data = []

    for id, row in routes_df.iterrows():
        i += 1
        for n in range(3):
            print(f"[{i}/{n}] Gerando frase para: {row['RouteStart']} -> {row['RouteEnd']}")

            phrase = agent.make_phrase(f"Origem: {row['RouteStart']}\nDestino: {row['RouteEnd']}\n")

            all_data.append({
                "RouteStart": row['RouteStart'],
                "RouteEnd": row['RouteEnd'],
                "llm_generated": phrase
            })
        print("\n")

    all_data = pd.DataFrame(all_data)
    all_data.to_csv(constants.DATA_FILE_PATH + 'llm_generated_routes_plus.csv', index=False)
    # routes_df.to_csv('llm_generated_routes_2.csv', index=False)
