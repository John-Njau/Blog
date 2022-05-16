import requests

def randomquote():
    quotes = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    if quotes.status_code == 200:
        quote = quotes.json()
        return quote

# import urllib.request
# import json
# from .models import Quote
#
# def configure_request(app):
#   global
