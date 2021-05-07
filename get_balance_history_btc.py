from genetic_get_wallet_balance import GettingBalanceData


class GetBalanceHistoryBTC(GettingBalanceData):
    def __init__(self, address):
        super(GetBalanceHistoryBTC, self).__init__()
        self.query = 'select * from btc_exchange_rate'
        self.address = address
        self.HTTP_request = f'https://blockchain.info/rawaddr/{self.address}'
        self.cost = {}
