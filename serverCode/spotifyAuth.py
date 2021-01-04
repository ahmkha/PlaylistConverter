import requests
from urllib.parse import urlencode
import os
from apiKeys import *

clientId = spotifyClientID
redirectURI = 'http://localhost:5000/SpotifyCallback'


def auth(request, response):
    scope = 'user-library-read'
    # state = os.urandom(16)
    queryStringDict = { 'client_id': clientId, 'response_type': 'token', 'redirect_uri': redirectURI, 'scope': scope, 'state': "123456789012345"}
    queryString = urlencode(queryStringDict)

    # response = requests.get('https://accounts.spotify.com/authorize?' + queryString)
    response = 'https://accounts.spotify.com/authorize?' + queryString
    return response

def callback(request, response):
    return None