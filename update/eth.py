import requests
from update.generic_retrieve_exchange_rate_class import RetrieveHourlyCryptoToUSDData


class UpdateETHExchangeRate(RetrieveHourlyCryptoToUSDData):
    def __init__(self):
        super(UpdateETHExchangeRate, self).__init__()
        self.currency = 'eth'
        self.api_address = 'https://api.etherscan.io/api?module=stats&action=ethprice'

    def retrieve_price_from_api(self):
        exchange_rate = requests.get(self.api_address).json()['result']['ethusd']
        self.insert_data_to_table(exchange_rate)


u = UpdateETHExchangeRate()
u.retrieve_price_from_api()
