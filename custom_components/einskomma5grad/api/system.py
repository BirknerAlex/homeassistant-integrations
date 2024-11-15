import requests
import datetime

from custom_components.einskomma5grad.api.client import Client
from custom_components.einskomma5grad.api.error import RequestError
from custom_components.einskomma5grad.api.ev_charger import EVCharger

class System:
    def __init__(self, client: Client, data: dict):
        self.client = client
        self.data = data

    def id(self) -> str:
        return self.data['id']

    def get_ev_chargers(self) -> EVCharger:
        res = requests.get(
            url = self.client.HEARTBEAT_API + "/api/v1/systems/"+ self.id() +"/devices/evs",
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.client.get_token(),
            })

        if res.status_code != 200:
            raise RequestError("Failed to get EV chargers: " + res.text)

        return res.json()['data']

    # Set the EMS mode of the system
    def set_ems_mode(self, auto: bool):
        res = requests.post(
            url = self.client.HEARTBEAT_API + "/api/v1/systems/"+ self.id() +"/ems/actions/set-manual-override",
            json = {
                "manualSettings": {},
                "overrideAutoSettings": auto == False
            },
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.client.get_token(),
            })

        if res.status_code != 201:
            raise RequestError("Failed to set EMS mode: " + res.text)

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