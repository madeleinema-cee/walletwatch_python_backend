import datetime as dt
from datetime import datetime, timedelta
import sqlite3
import requests

class Data:
    def __init__(self, address):
        self.start_date = dt.datetime(2013, 1, 1, 00, 00)
        self.end_date = dt.datetime.now()
        self.address = address
        self.dates_marker = None
        self.query = 'select * from btc_usd_exchange_rate'
        self.conn = sqlite3.connect('btc_usd_exchange_rate.db')
        self.cursor = self.conn.cursor()
        self.balance_history = {}
        self.transaction_history = {}
        self.cost = {}
        self.btc_balance = None

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
        HTTP_request = f'https://blockchain.info/rawaddr/{self.address}'
        response = requests.get(HTTP_request).json()

        for transaction in response['txs']:
            time = dt.datetime.fromtimestamp(transaction['time']).strftime('%Y-%m-%d %H:00:00')
            self.transaction_history[time] = transaction['result'] / 100000000
            transactions.append(transaction['result'] / 100000000)
            dates.append(time)
        new_dates = dates[:: -1]
        new_transactions = transactions[:: -1]

        for new_transaction in new_transactions:
            c.append(new_transaction)
            balances.append(sum(c))
        self.btc_balance = balances[-1]

        self.dates_marker = new_dates

        self.start_date = new_dates[0]

        return new_dates, balances

    def find_balance_history(self):
        x, y = self.find_transaction_data()
        for transaction_date in x:
            for balance in y:
                self.balance_history[transaction_date] = balance
                y.remove(balance)
                break

    def generate_days(self):
        delta = timedelta(hours=1)
        new = datetime.strptime(self.start_date, "%Y-%m-%d %H:00:00")

        while new < self.end_date:
            yield new
            new += delta

    def insert_balance_history_to_dates(self):
        self.find_balance_history()
        balance = {}

        for single_date in self.generate_days():
            balance[single_date.strftime("%Y-%m-%d %H:00:00")] = 0

        for balance_date in balance.keys():
            if balance_date in self.balance_history.keys():
                balance[balance_date] = self.balance_history[balance_date]
            else:
                if balance[balance_date] == 0:
                    last_hour_datetime = dt.datetime.strptime(balance_date, '%Y-%m-%d %H:00:00') - timedelta(hours=1)
                    value = balance[str(last_hour_datetime)]
                    balance[balance_date] = value
        return balance

    def convert_balance_to_usd(self):
        hourly_balance = self.insert_balance_history_to_dates()
        results = self.fetchall(self.query)
        d = dict(results)

        for date in d.keys():
            if date in hourly_balance:
                hourly_balance[date] *= float(d[date])

            if date in self.transaction_history:
                self.cost[date] = float(self.transaction_history[date] * d[date])
        return hourly_balance

    def get_balance_data(self):
        data = {}
        balance = []
        hourly_balance = self.convert_balance_to_usd()
        for key, value in hourly_balance.items():
            d = {'x': key, 'y': value}
            balance.append(d)

        data['balance'] = balance
        HTTP_request = 'https://blockchain.info/ticker'
        response = requests.get(HTTP_request).json()
        currency_exchange_rate_usd = response['USD']['15m']
        data['btctousd'] = currency_exchange_rate_usd
        data['transactionhistory'] = self.transaction_history
        total_invested = sum(value for value in self.cost.values() if value > 0)
        total_profit_from_selling = abs(sum(value for value in self.cost.values() if value < 0))
        total_profit = total_profit_from_selling + balance[-1]['y'] - total_invested
        data['totalprofit'] = total_profit
        data['totalinvested'] = total_invested
        data['btcbalance'] = self.btc_balance
        profit_margin = total_profit/total_invested * 100
        data['profitmargin'] = profit_margin

        return data
