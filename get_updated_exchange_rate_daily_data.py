import requests
from datetime import datetime
from helpers.db import ExchangeRateDb


class RetrieveHourlyCryptoToUSDData:
    def __init__(self):
        self.db_path = 'helpers/cryptocurrency_exchange_rate.db'
        self.db = ExchangeRateDb(self.db_path)
        self.currency = None

    def main(self):
        self.retrieve_price_from_api()

    def retrieve_price_from_api(self):
        pass

    def insert_data_to_table(self, exchange_rate):
        updated_time = datetime.now().strftime('%Y-%m-%d')
        query = f'''
        insert into {self.currency}_exchange_rate (date, '{self.currency}')
        values ('{updated_time}', '{exchange_rate}')
        '''
        self.db.execute(query=query)


class ETHToUSDData(RetrieveHourlyCryptoToUSDData):
    def __init__(self):
        super(ETHToUSDData, self).__init__()
        self.currency = 'eth'
        self.api_address = 'https://api.etherscan.io/api?module=stats&action=ethprice'

    def retrieve_price_from_api(self): # this is the btc one
        exchange_rate = requests.get(self.api_address).json()['bpi']['USD']['rate_float']
        self.insert_data_to_table(exchange_rate)


r = RetrieveHourlyCryptoToUSDData()
r.retrieve_price_from_api()
e = ETHToUSDData()
e.retrieve_price_from_api()
