import requests

def openURL(URL, params):
    r = requests.get(URL + "?", params=params)
    return r.text