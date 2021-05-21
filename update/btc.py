import requests
from update.generic_retrieve_exchange_rate_class import RetrieveHourlyCryptoToUSDData


class UpdateBTCExchangeRate(RetrieveHourlyCryptoToUSDData):
    def __init__(self):
        super(UpdateBTCExchangeRate, self).__init__()
        self.currency = 'btc'
        self.api_address = 'https://api.coindesk.com/v1/bpi/currentprice.json'

    def retrieve_price_from_api(self):  # this is the btc one
        exchange_rate = requests.get(self.api_address).json()['bpi']['USD']['rate_float']
        self.insert_data_to_table(exchange_rate)


u = UpdateBTCExchangeRate()
u.retrieve_price_from_api()
