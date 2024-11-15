import requests
import datetime

from custom_components.einskomma5grad.api.client import Client
from custom_components.einskomma5grad.api.error import RequestError

class System:
    def __init__(self, client: Client, data: dict):
        self.client = client
        self.data = data

    def id(self) -> str:
        return self.data['id']

    def get_prices(self, start: datetime, end: datetime):
        res = requests.get(
            url = self.client.HEARTBEAT_API + "/api/v1/systems/"+ self.id() +"/charts/market-prices",
            params = {
                "from": start.strftime("%Y-%m-%d"),
                "to": end.strftime("%Y-%m-%d"),
                "resolution": "1h",
            },
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.client.get_token(),
            })

        if res.status_code != 200:
            raise RequestError("Failed to get prices: " + res.text)

        return res.json()['energyMarketWithGridCosts']['data']