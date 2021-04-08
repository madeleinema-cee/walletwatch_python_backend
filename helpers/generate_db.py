import csv

from db import ExchangeRateDb
import pandas as pd


class GenerateDatabase:
    def __init__(self):
        self.db_path = 'cryptocurrency_exchange_rate.db'
        self.db = ExchangeRateDb(self.db_path)

    def main(self):
        self.create_exchange_rate_table()
        self.insert_data_from_csv()

    def create_exchange_rate_table(self):
        query = """
        create table exchange_rate
        (date, btc_close, eth_close)
        """
        self.db.execute(query)

    def insert_data_from_csv(self):
        btc = pd.read_csv('gemini_BTCUSD_day.csv')
        eth = pd.read_csv('gemini_ETHUSD_day.csv')
        merged = btc.merge(eth, on='Date')
        merged.to_csv('exchange_rate.csv', index=False)

        with open('exchange_rate.csv', 'r') as file:
            next(file)
            reader1 = csv.reader(file)
            for line in reader1:
                date = line[1]
                btc_close = line[6]
                eth_close = line[-2]
                self.insert_btc_rate(date, btc_close, eth_close)

    def insert_btc_rate(self, date, btc_close, eth_close):
        query = f'''
        insert into exchange_rate (date, btc_close, eth_close)
        values ('{date}', '{btc_close}', '{eth_close}')
        '''
        self.db.execute(query)


g = GenerateDatabase()
g.main()

