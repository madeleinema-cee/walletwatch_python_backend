import csv
from datetime import datetime

from db import ExchangeRateDb


class GenerateDatabase:
    def __init__(self):
        self.db_path = 'cryptocurrency_exchange_rate.db'
        self.db = ExchangeRateDb(self.db_path)

    def main(self):
        self.create_exchange_rate_table()
        self.insert_data_from_csv()

    def create_exchange_rate_table(self):
        query = """
        create table btc_exchange_rate
        (date, btc_close)
        """
        self.db.execute(query)

    def insert_data_from_csv(self):
        # eth = pd.read_csv('gemini_ETHUSD_day.csv')
        # merged = btc.merge(eth, on='Date')
        # merged.to_csv('exchange_rate.csv', index=False)

        with open('gemini_BTCUSD_day.csv', 'r') as file:
            next(file)
            reader1 = csv.reader(file)
            for line in reader1:
                date = datetime.strptime(line[1], '%Y-%m-%d %H:00:00').strftime('%Y-%m-%d')
                btc_close = line[6]
                self.insert_btc_rate(date, btc_close)

    def insert_btc_rate(self, date, btc_close):
        query = f'''
        insert into btc_exchange_rate (date, btc_close)
        values ('{date}', '{btc_close}')
        '''
        self.db.execute(query)


g = GenerateDatabase()
g.main()

