import datetime as dt
import requests
from genetic_get_wallet_balance import GettingBalanceData


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

    def retrieve_data_from_api(self):
        response = requests.get(self.HTTP_request).json()

        balance_history = {}
        transactions = []
        balances = []
        for transaction in response['result']:
            time = dt.datetime.fromtimestamp(int(transaction['timeStamp'])).strftime('%Y-%m-%d')
            print(int(transaction['value'])/ 1000000000000000000)
            transactions.append(int(transaction['value']) / 1000000000000000000)
            balances.append(sum(transactions))
            for balance in balances:
                balance_history[time] = balance
                balances.remove(balance)
                break
            self.transaction_history[time] = int(transaction['value']) / 1000000000000000000
        print(balance_history)
        self.get_final_balance()
        return self.get_balance_data(balance_history)

    def get_final_balance(self):
        HTTP_request = f'https://api.etherscan.io/api?module=account&action=balance&address={self.address}' \
                       f'&tag=latest&apikey=MSH91WI3EYPAXNEUA7EMQ28Z13TW3MMYWK'
        response = requests.get(HTTP_request).json()
        self.balance = int(response['result']) / 1000000000000000000



