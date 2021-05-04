import datetime as dt
import requests
from genetic_get_wallet_balance import GettingBalanceData


class RetrievingBTCBalanceData(GettingBalanceData):
    def __init__(self, address):
        super(RetrievingBTCBalanceData, self).__init__()
        self.address = address
        self.query = 'select * from btc_exchange_rate'
        self.HTTP_request = f'https://blockchain.info/rawaddr/{address}'

    def retrieve_data_from_api(self):
        response = requests.get(self.HTTP_request).json()
        # response = test_result
        self.btc_balance = response['final_balance']
        balance_history = {}
        for balance in reversed(response['txs']):
            time = dt.datetime.fromtimestamp(balance['time']).strftime('%Y-%m-%d')
            balance_history[time] = balance['balance'] / 100000000
            self.transaction_history[time] = balance['result'] / 100000000
        self.get_balance_data(balance_history)


r = RetrievingBTCBalanceData(address='3KYwVvvvfNApEDjnVjgQU4swmSPhNKCzwD')
r.retrieve_data_from_api()
