import csv
from datetime import datetime
from helpers.db import ExchangeRateDb


class GenerateDatabase:
    def __init__(self, currency, file):
        self.db_path = 'helpers/cryptocurrency_exchange_rate.db'
        self.db = ExchangeRateDb(self.db_path)
        self.currency = currency
        self.file = file

    def main(self):
        self.create_exchange_rate_table()
        self.insert_data_from_csv()

    def create_exchange_rate_table(self):
        query = f"""
        create table {self.currency}_exchange_rate
        (date, '{self.currency}')
        """
        self.db.execute(query)

    def insert_data_from_csv(self):
        with open(self.file, 'r') as file:
            next(file)
            reader1 = csv.reader(file)
            for line in reader1:
                date = datetime.strptime(line[1], '%Y-%m-%d %H:00:00')
                close = line[6]
                self.insert_currency_rate(date, close)

    def insert_currency_rate(self, date, close):
        query = f'''
        insert into {self.currency}_exchange_rate (date, '{self.currency}')
        values ('{date}', '{close}')
        '''
        self.db.execute(query)


class ETHDatabase(GenerateDatabase):
    def __init__(self, currency, file):
        super().__init__(currency, file)


g = GenerateDatabase('btc', 'helpers/gemini_BTCUSD_1hr.csv')
g.main()
e = ETHDatabase('eth', 'helpers/gemini_ETHUSD_1hr.csv')
e.main()
