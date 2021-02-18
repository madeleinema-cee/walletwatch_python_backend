from flask import jsonify, request
from api import app
from get_historical_btc_usd_hourly_data import ExchangeRateDb

database = ExchangeRateDb('btc_usd_exchange_rate.db')
exchange_rates = database.fetchall(query='select * from btc_usd_exchange_rate ')


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Historical Exchange Rates (BTC-USD)</h1>'''


@app.route('/api/exchange_rates/btc/all', methods=['GET'])
def api_all():
    return jsonify(exchange_rates)


@app.route('/api/exchange_rates/btc', methods=['GET'])
def api_id():
    # Check if an date was provided as part of the URL.
    # If date is provided, assign it to a variable.
    # If no date is provided, display an error in the browser.
    if 'date' in request.args:
        date = request.args['date']
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for results
    results = []

    # Loop through the data and match results that fit the requested date.
    # dates are unique
    for exchange_rate in exchange_rates:
        if exchange_rate['date'] == date:
            results.append(exchange_rate)

    return jsonify(results)
