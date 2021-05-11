import datetime as dt
from datetime import datetime, timedelta
import requests
from helpers.db import ExchangeRateDb


class GettingBalanceData:
    def __init__(self):
        self.start_date = dt.datetime(2013, 1, 1, 00, 00)
        self.end_date = dt.datetime.now()
        self.address = None
        self.query = None
        self.db_path = 'helpers/cryptocurrency_exchange_rate.db'
        self.db = ExchangeRateDb(self.db_path)
        self.HTTP_request = None
        self.transaction_history = {}
        self.cost = {}
        self.balance = None
        self.token = None
        self.HTTP_request_currency_exchange = None

    def generate_days(self, balance_history):
        self.start_date = list(balance_history.keys())[0]
        delta = timedelta(hours=1)
        new = datetime.strptime(self.start_date, "%Y-%m-%d")

        while new < self.end_date:
            yield new
            new += delta

    def insert_balance_history_to_dates(self, balance_history):
        balance = {}

        for single_date in self.generate_days(balance_history):
            balance[single_date.strftime("%Y-%m-%d")] = None

        for balance_date in balance.keys():
            if balance_date in balance_history.keys():
                balance[balance_date] = balance_history[balance_date]
            else:
                if balance[balance_date] is None:
                    last_day_datetime = (dt.datetime.strptime(balance_date, '%Y-%m-%d')
                                         - timedelta(hours=1)).strftime('%Y-%m-%d')
                    value = balance[str(last_day_datetime)]
                    balance[balance_date] = value
        return balance

    def convert_balance_to_usd(self, balance_history):
        hourly_balance = self.insert_balance_history_to_dates(balance_history)
        results = self.db.fetchall(self.query)

        for result in results:
            if result['date'] in hourly_balance:
                hourly_balance[result['date']] *= float(result[self.token])

            if result['date'] in self.transaction_history:
                self.cost[result['date']] = self.transaction_history[result['date']] * float(result[self.token])
                print(self.cost)

        return hourly_balance

    def get_balance_data(self, balance_history):
        data = {}
        balance = []
        hourly_balance = self.convert_balance_to_usd(balance_history)
        for key, value in hourly_balance.items():
            d = {'x': key, 'y': value}
            balance.append(d)

        data['balance'] = balance
        response = requests.get(self.HTTP_request_currency_exchange).json()
        currency_exchange_rate_usd = response['USD']
        data['tousd'] = currency_exchange_rate_usd
        data['transactionhistory'] = self.transaction_history
        total_invested = sum(value for value in self.cost.values() if value > 0)
        total_profit_from_selling = abs(sum(value for value in self.cost.values() if value < 0))
        total_profit = total_profit_from_selling + balance[-1]['y'] - total_invested
        data['total_profit'] = total_profit
        data['total_invested'] = total_invested
        data['profit_margin'] = total_profit / total_invested * 100
        data['final_balance'] = self.balance
        return data
