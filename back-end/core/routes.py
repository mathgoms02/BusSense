import requests
import pandas as pd


class RouteFetcher:
    def __init__(self, url: str):
        self.url = url

    def fetch_routes(self) -> pd.DataFrame:
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df = df[['route_short_name', 'route_name_start', 'route_name_end']]
            df.columns = ['RouteCode', 'RouteStart', 'RouteEnd']
            return df
        else:
            raise Exception(f"API Error: {response.status_code}")
