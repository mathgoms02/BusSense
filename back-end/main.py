import os
import pandas as pd
import requests
from dotenv import load_dotenv
from model.gemini_analysis import GeminiThinking

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

    assistant = GeminiThinking(api_key=api_key, routes_data=routes_df)
    assistant.run()
