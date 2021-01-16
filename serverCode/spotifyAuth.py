import requests
from urllib.parse import urlencode
import os
from apiKeys import *

clientId = spotifyClientID
secretKey = spotifyClientSecret
authRedirectURI = 'http://localhost:5000/SpotifyCallback'


def auth():
    scope = 'user-library-read'
    # state = os.urandom(16) # will change to actual random 16 character state
    queryStringDict = { 'client_id': clientId, 'response_type': 'code', 'redirect_uri': authRedirectURI, 'scope': scope, 'state': "123456789012345"}
    queryString = urlencode(queryStringDict)

    response = 'https://accounts.spotify.com/authorize?' + queryString
    return response

def callback(code):
    response = requests.post('https://accounts.spotify.com/api/token', \
        data={'grant_type': 'authorization_code', 'code': code, 'redirect_uri': authRedirectURI, 'client_id': clientId, 'client_secret': secretKey})
    return response

def getCurrentUser(accessToken):
    headers = {'Authorization': 'Bearer ' + str(accessToken)}
    response = requests.get('https://api.spotify.com/v1/me/playlists', headers = headers)
    return response