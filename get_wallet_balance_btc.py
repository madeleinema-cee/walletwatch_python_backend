import datetime as dt
import requests
from generic_get_wallet_balance import GettingBalanceData


class RetrievingBTCBalanceData(GettingBalanceData):
    def __init__(self, address):
        super(RetrievingBTCBalanceData, self).__init__()
        self.address = address
        self.query = 'select * from btc_exchange_rate'
        self.HTTP_request = f'https://blockchain.info/rawaddr/{address}'
        self.token = 'btc'
        self.HTTP_request_currency_exchange = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD'
        self.time = None

    def retrieve_data_from_api(self):
        response = requests.get(self.HTTP_request).json()
        # response = test_result
        self.balance = response['final_balance'] / 100000000
        balance_history = {}
        for balance in reversed(response['txs']):
            self.time = dt.datetime.fromtimestamp(balance['time']).strftime('%Y-%m-%d %H:00:00')
            balance_history[self.time] = balance['balance'] / 100000000
            print(balance['balance'] / 100000000)
            self.get_transaction_history(balance['result'] / 100000000)

        return self.get_balance_data(balance_history)

    def get_transaction_history(self, value):
        if self.time not in self.transaction_history:
            self.transaction_history[self.time] = [value]
        else:
            self.transaction_history[self.time].append(value)

