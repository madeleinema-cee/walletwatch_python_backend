import requests
from datetime import datetime
from helpers.db import ExchangeRateDb


class RetrieveHourlyBTCToUSDData:
    def __init__(self):
        self.db_path = 'helpers/cryptocurrency_exchange_rate.db'
        self.db = ExchangeRateDb(self.db_path)

    def retrieve_price_from_api(self):
        HTTP_request = 'https://api.coindesk.com/v1/bpi/currentprice.json'
        response = requests.get(HTTP_request).json()
        btc_rate = response['bpi']['USD']['rate_float']
        HTTP_request2 = 'https://api.etherscan.io/api?module=stats&action=ethprice'
        response2 = requests.get(HTTP_request2).json()
        eth_rate = response2['result']['ethusd']
        updated_time = datetime.now().strftime('%Y-%m-%d')
        query = f'''
        insert into btc_exchange_rate (date, btc_close)
        values ('{updated_time}', '{btc_rate}')
        '''
        self.db.execute(query=query)


h = RetrieveHourlyBTCToUSDData()
h.retrieve_price_from_api()