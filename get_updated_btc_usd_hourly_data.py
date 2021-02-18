import requests
import sqlite3
import time
from datetime import datetime


class RetrieveHourlyBTCToUSDData:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def execute(self, query, project):
        self.cursor.execute(query, project)
        self.conn.commit()

    def fetchall(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        result = [dict(row) for row in self.cursor.fetchall()]
        return result

    def close(self):
        self.conn.close()

    def retrieve_data_from_coindesk_api(self):
        HTTP_request = 'https://api.coindesk.com/v1/bpi/currentprice.json'
        response = requests.get(HTTP_request).json()
        rate = response['bpi']['USD']['rate_float']
        updated_time = datetime.now().strftime('%Y-%m-%d/%H:00:00')

        query = '''insert into btc_usd_exchange_rate values (?, ?)'''
        project = (updated_time, rate)
        self.execute(query=query, project=project)


h = RetrieveHourlyBTCToUSDData('btc_usd_exchange_rate.db')
h.retrieve_data_from_coindesk_api()