import datetime as dt
import requests
from generic_get_wallet_balance import GettingBalanceData


test_result = {
  "status": "1",
  "message": "OK",
  "result": [
    {
      "blockNumber": "11564709",
      "timeStamp": "1609455170",
      "hash": "0x92e6f5cd5cdb286eb22535f7ec04992b082ee7bca19ab65a7ec58ad47dd96286",
      "nonce": "0",
      "blockHash": "0x0a82c801255d82d6750d94e6208e50fc71222fa33691e2ef664ff15c73ac1334",
      "transactionIndex": "74",
      "from": "0x231e48dd30a5236c9efcf5e14c487d566ee5b04b",
      "to": "0x3e8cf94e18ec6cf7e8a4c0ad83518d3dbd7461d6",
      "value": "513513630000000000",
      "gas": "21000",
      "gasPrice": "56000000000",
      "isError": "0",
      "txreceipt_status": "1",
      "input": "0x",
      "contractAddress": "",
      "cumulativeGasUsed": "4041686",
      "gasUsed": "21000",
      "confirmations": "861772"
    },
    {
      "blockNumber": "11610396",
      "timeStamp": "1610060794",
      "hash": "0xd617c69f68a1f52128aea68702a2f7dd0f425e9e0bd36254e7bd1fa0c15479f4",
      "nonce": "0",
      "blockHash": "0x3a34f83fb7a0060d2b41242e8a657d3f55862d266bd5dd33c8220f6c90e069f9",
      "transactionIndex": "237",
      "from": "0x7f4cdc22ce07edd2f59a6c364083c46a48d36217",
      "to": "0x3e8cf94e18ec6cf7e8a4c0ad83518d3dbd7461d6",
      "value": "271064830000000000",
      "gas": "21000",
      "gasPrice": "123000000000",
      "isError": "0",
      "txreceipt_status": "1",
      "input": "0x",
      "contractAddress": "",
      "cumulativeGasUsed": "11715354",
      "gasUsed": "21000",
      "confirmations": "816085"
    },
    {
      "blockNumber": "11611386",
      "timeStamp": "1610073849",
      "hash": "0x28e5a53b1dec8f5fc2f65e0f50428c67644039c989498373404108e372158644",
      "nonce": "0",
      "blockHash": "0x9cee94524ccef3020e347127c850790cc7fee768a00d1499093ba1c19807855f",
      "transactionIndex": "154",
      "from": "0xb6941229ba8bce742636817d158f631bad706a35",
      "to": "0x3e8cf94e18ec6cf7e8a4c0ad83518d3dbd7461d6",
      "value": "210801540000000000",
      "gas": "21000",
      "gasPrice": "270000000000",
      "isError": "0",
      "txreceipt_status": "1",
      "input": "0x",
      "contractAddress": "",
      "cumulativeGasUsed": "12476030",
      "gasUsed": "21000",
      "confirmations": "815095"
    },
    {
      "blockNumber": "11668288",
      "timeStamp": "1610827599",
      "hash": "0xed0d0c0e90e7d4715508e990897b8896a9ba64f52511ee97512d99f9611eaa3f",
      "nonce": "0",
      "blockHash": "0x0a5f6ba479186a11cea719085c44f31f9ba3c9d74cd4aa1d3c9c141c2f0effae",
      "transactionIndex": "51",
      "from": "0x7596f86ca7382bc258d3c26d8e9dcd395ea4082d",
      "to": "0x3e8cf94e18ec6cf7e8a4c0ad83518d3dbd7461d6",
      "value": "1998110000000000000",
      "gas": "21000",
      "gasPrice": "90000000000",
      "isError": "0",
      "txreceipt_status": "1",
      "input": "0x",
      "contractAddress": "",
      "cumulativeGasUsed": "2662058",
      "gasUsed": "21000",
      "confirmations": "758193"
    },
    {
      "blockNumber": "11670650",
      "timeStamp": "1610858928",
      "hash": "0x56686260a46e6764fbc36bcb3f55c98e918c04bd5f43221f4b37e1be521ba0cc",
      "nonce": "0",
      "blockHash": "0xed43ff428b7a4e56037138a09e7292dafa498b3c6c093b7b5ac85aff3213d764",
      "transactionIndex": "30",
      "from": "0xe3aff805a4e503d2a62c57edfb195c8f738c7d3c",
      "to": "0x3e8cf94e18ec6cf7e8a4c0ad83518d3dbd7461d6",
      "value": "393418950000000000",
      "gas": "21000",
      "gasPrice": "50000000000",
      "isError": "0",
      "txreceipt_status": "1",
      "input": "0x",
      "contractAddress": "",
      "cumulativeGasUsed": "1896560",
      "gasUsed": "21000",
      "confirmations": "755831"
    }
  ]
}

class RetrievingETHBalanceData(GettingBalanceData):
    def __init__(self, address):
        super(RetrievingETHBalanceData, self).__init__()
        self.address = address
        self.query = 'select * from eth_exchange_rate'
        self.HTTP_request = f'https://api.ethself.erscan.io/api?module=account&action=txlist' \
                            f'&address={self.address}&endblock=99999999&sort=asc' \
                            f'&apikey=MSH91WI3EYPAXNEUA7EMQ28Z13TW3MMYWK'
        self.token = 'eth'
        self.HTTP_request_currency_exchange = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD'
        self.time = None

    def retrieve_data_from_api(self):
        response = test_result

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



