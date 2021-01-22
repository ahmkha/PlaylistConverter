import requests
import re
from urllib.parse import urlencode
import os
from apiKeys import youtube_client_id, youtube_project_id, youtube_client_secret
import google.oauth2.credentials
import google_auth_oauthlib.flow


def auth():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        os.path.join(os.path.dirname(__file__), 'yt_client_tokens.json'),
        scopes=['https://www.googleapis.com/auth/youtube'])
    flow.redirect_uri = 'http://localhost:5000/YoutubeCallback'
    authorization_url = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    return authorization_url[0]

def callback(code):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        os.path.join(os.path.dirname(__file__), 'yt_client_tokens.json'),
        scopes=['https://www.googleapis.com/auth/youtube'])
    flow.redirect_uri = 'http://localhost:5000/YoutubeCallback'

    authorization_response = code
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    return credentials.token
