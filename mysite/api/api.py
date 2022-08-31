import requests
from alpha_vantage.timeseries import TimeSeries

key='HB0SZP3CESKT6SQQ'
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=${key}'
r = requests.get(url)
data = r.json()


ts = TimeSeries(key=key, output_format='JSON')

# Get json object with the intraday data and another with  the call's metadata