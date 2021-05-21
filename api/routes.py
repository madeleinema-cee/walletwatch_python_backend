from flask import jsonify, request
from api import app
from get_wallet_balance_btc import RetrievingBTCBalanceData
from get_wallet_balance_eth import RetrievingETHBalanceData


@app.route('/', methods=['GET'])
def home():
    return '''<h1>WalletWatch API</h1>'''


@app.route('/api/<string:currency>', methods=['GET'])
def get_balance_data(currency):
    # Check if an date was provided as part of the URL.
    # If date is provided, assign it to a variable.
    # If no date is provided, display an error in the browser.
    if 'address' in request.args:
        address = request.args['address']
        if currency == 'btc':
            retrieve_btc_data = RetrievingBTCBalanceData(address)
            data = retrieve_btc_data.retrieve_data_from_api()
            return jsonify(data)
        elif currency == 'eth':
            retrieve_eth_data = RetrievingETHBalanceData(address)
            data = retrieve_eth_data.retrieve_data_from_api()
            return jsonify(data)
    else:
        return "Error: No information for this address. Please specify a valid address."
