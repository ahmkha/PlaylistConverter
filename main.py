import sys
from flask import Flask, render_template, url_for, redirect, request, make_response
sys.path.insert(1, 'serverCode')
from serverCode import spotifyAuth

app = Flask(__name__)
spotify_access_token = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/SpotifyToYT')
def spotifyToIndex():
    return render_template('spotifyToYT.html')

@app.route('/YTToSpotify')
def ytToSpotify():
    return 'YTToSpotify'

@app.route('/SpotifyLogin')
def spotifyLogin():
    return redirect(spotifyAuth.auth())

@app.route('/SpotifyCallback')
def spotifyCallback():
    codeParam = request.args.get('code')
    # Also check if state has changed as well later
    if codeParam == None:
        return "Bro, you're buggin..."
    authedPage = spotifyAuth.callback(str(codeParam))
    # return authedPage.json()
    global spotify_access_token 
    spotify_access_token = authedPage.json()['access_token']
    return redirect('/SpotifyAuthed')

@app.route('/SpotifyAuthed')
def spotifyAuthed():
    global spotify_access_token
    currentUserPlaylists = spotifyAuth.getCurrentUser(spotify_access_token).json()['items']
    return render_template('spotifyPlaylistView.html', playlists=currentUserPlaylists)

if __name__ == "__main__":
    app.run(debug=True)