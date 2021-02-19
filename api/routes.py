from flask import jsonify, request, abort
from api import app
from get_wallet_balance_btc_to_usd import Data


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Historical Exchange Rates (BTC-USD)</h1>'''


@app.route('/api/btc', methods=['GET'])
def api_id():
    # Check if an date was provided as part of the URL.
    # If date is provided, assign it to a variable.
    # If no date is provided, display an error in the browser.
    if 'address' in request.args:
        address = request.args['address']
        d = Data(address)
        data = d.plot_hourly_balance_data()
        return jsonify(data)
    else:
        return "Error: No address field provided. Please specify an address."


