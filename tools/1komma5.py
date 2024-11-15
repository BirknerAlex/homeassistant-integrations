import os
import sys
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from custom_components.einskomma5grad.api.client import Api

def main():
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    api_client = Api(username, password)



    print(api_client.get_token())
    print(api_client.get_token_parsed())
    print(api_client.get_user())
    print(api_client.get_systems())

    systems = api_client.get_systems()

    system = systems[0]

    start = datetime.date.today()
    end = start + datetime.timedelta(days=1)
    prices =  api_client.get_prices(system["id"], start, end)

    print(prices)
    print(api_client.close())

if __name__ == "__main__":
    main()