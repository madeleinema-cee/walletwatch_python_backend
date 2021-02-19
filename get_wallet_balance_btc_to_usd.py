import datetime as dt
from datetime import datetime, timedelta
import sqlite3



class Data:
    def __init__(self, address):
        self.start_date = dt.datetime(2013, 1, 1, 00, 00)
        self.end_date = dt.datetime.now()
        self.address = address
        self.dates_marker = None
        self.query = 'select * from btc_usd_exchange_rate'
        self.conn = sqlite3.connect('btc_usd_exchange_rate.db')
        self.cursor = self.conn.cursor()

    def execute(self, query, project):
        self.cursor.execute(query, project)
        self.conn.commit()

    def fetchall(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result

    def close(self):
        self.conn.close()

    def find_transaction_data(self):
        transactions = []
        dates = []
        c = []
        balances = []
        # HTTP_request = f'https://blockchain.info/rawaddr/{self.address}'
        response = test_result

        for transaction in response['txs']:
            time = dt.datetime.fromtimestamp(transaction['time']).strftime('%Y-%m-%d %H:00:00')
            transactions.append(transaction['result'] / 100000000)
            dates.append(time)
        new_dates = dates[:: -1]
        new_transactions = transactions[:: -1]

        for new_transaction in new_transactions:
            c.append(new_transaction)
            balances.append(sum(c))

        self.dates_marker = new_dates

        self.start_date = new_dates[0]

        return new_dates, balances

    def find_balance_history(self):
        x, y = self.find_transaction_data()
        balance_history = {}

        for transaction_date in x:
            for balance in y:
                balance_history[transaction_date] = balance
                y.remove(balance)
                break

        return balance_history

    def generate_days(self):
        delta = timedelta(hours=1)
        new = datetime.strptime(self.start_date, "%Y-%m-%d %H:00:00")

        while new < self.end_date:
            yield new
            new += delta

    def insert_balance_history_to_dates(self):
        balance_history = self.find_balance_history()
        balance = {}

        for single_date in self.generate_days():
            balance[single_date.strftime("%Y-%m-%d %H:00:00")] = 0

        for balance_date in balance_history.keys():
            for date in balance.keys():
                if balance_date == date:
                    balance[balance_date] = balance_history[balance_date]

        return balance

    def apply_balance_history_to_everyday(self):
        balance = self.insert_balance_history_to_dates()
        d = list(balance.keys())

        for date in d[1:]:
            if balance[date] == 0:
                last_hour_datetime = dt.datetime.strptime(date, '%Y-%m-%d %H:00:00') - timedelta(hours=1)
                value = balance[str(last_hour_datetime)]
                balance[date] = value

        return balance

    def convert_balance_to_usd(self):
        hourly_balance = self.apply_balance_history_to_everyday()
        results = self.fetchall(self.query)
        d = dict(results)
        for date in d.keys():
            if date in hourly_balance:
                hourly_balance[date] *= float(d[date])
        return hourly_balance

    def plot_hourly_balance_data(self):
        hourly_balance = self.convert_balance_to_usd()
        return hourly_balance



