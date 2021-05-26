import datetime as dt
import requests
from generic_get_wallet_balance import GettingBalanceData


class RetrievingETHBalanceData(GettingBalanceData):
    def __init__(self, address):
        super(RetrievingETHBalanceData, self).__init__()
        self.address = address
        self.query = 'select * from eth_exchange_rate'
        self.HTTP_request = f'https://api.etherscan.io/api?module=account&action=txlist' \
                            f'&address={self.address}&endblock=99999999&sort=asc' \
                            f'&apikey=MSH91WI3EYPAXNEUA7EMQ28Z13TW3MMYWK'
        self.token = 'eth'
        self.HTTP_request_currency_exchange = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD'
        self.time = None

    def retrieve_data_from_api(self):
        response = requests.get(self.HTTP_request).json()
        # response = test_result

        balance_history = {}
        transactions = []
        balances = []

        for transaction in response['result']:
            self.time = dt.datetime.fromtimestamp(int(transaction['timeStamp'])).strftime('%Y-%m-%d %H:00:00')
            if transaction['to'] == self.address.lower():
                value = int(transaction['value']) / 1000000000000000000
                transactions.append(value)
                self.get_transaction_history(value)
            else:
                value = int(transaction['value']) / 1000000000000000000 * -1
                transactions.append(value)
                self.get_transaction_history(value)

            balances.append(sum(transactions))
            for balance in balances:
                balance_history[self.time] = balance
                balances.remove(balance)
                break

        self.get_final_balance()
        return self.get_balance_data(balance_history)

    def get_transaction_history(self, value):
        if self.time not in self.transaction_history:
            self.transaction_history[self.time] = [value]
        else:
            self.transaction_history[self.time].append(value)

    def get_final_balance(self):
        HTTP_request = f'https://api.etherscan.io/api?module=account&action=balance&address={self.address}' \
                       f'&tag=latest&apikey=MSH91WI3EYPAXNEUA7EMQ28Z13TW3MMYWK'
        response = requests.get(HTTP_request).json()
        self.balance = int(response['result']) / 1000000000000000000
