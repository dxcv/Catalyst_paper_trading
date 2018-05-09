import requests

url = "https://api.bitfinex.com/v1/symbols_details"

response = requests.request("GET", url)

print(response.text)