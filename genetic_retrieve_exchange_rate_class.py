import requests
from datetime import datetime
from helpers.db import ExchangeRateDb


class RetrieveHourlyCryptoToUSDData:
    def __init__(self):
        self.db_path = '../helpers/cryptocurrency_exchange_rate.db'
        self.db = ExchangeRateDb(self.db_path)
        self.currency = None

    def insert_data_to_table(self, exchange_rate):
        updated_time = datetime.now().strftime('%Y-%m-%d')
        query = f'''
        insert into {self.currency}_exchange_rate (date, '{self.currency}')
        values ('{updated_time}', '{exchange_rate}')
        '''
        self.db.execute(query=query)





