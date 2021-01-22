import sys
from flask import Flask, render_template, url_for, redirect, request, make_response
sys.path.insert(1, 'serverCode')
from serverCode import spotifyAuth, youtubeAuth

app = Flask(__name__)
spotify_access_token = ''
youtube_access_token = ''

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
    global spotify_access_token 
    spotify_access_token = authedPage.json()['access_token']
    return redirect('/SpotifyAuthed')

@app.route('/SpotifyAuthed', methods=['GET', 'POST'])
def spotifyAuthed():
    global spotify_access_token
    if request.method == 'GET':
        currentUserPlaylists = spotifyAuth.getCurrentUser(spotify_access_token).json()['items']
        return render_template('spotifyPlaylistView.html', playlists=currentUserPlaylists)
    else:
        selectedPlaylist = request.form['playlist']
        playlistInfo = spotifyAuth.getTracks(spotify_access_token, selectedPlaylist)
        tracks = playlistInfo['items']
        return render_template('spotifyTracksView.html', tracks=tracks)

@app.route('/YoutubeLogin', methods=['GET', 'POST'])
def youtubeLogin():
    # return request.form.getlist('tracks')
    return redirect(youtubeAuth.auth())

@app.route('/YoutubeCallback')
def youtubeCallback():
    codeParam = request.url
    # Also check if state has changed as well later
    if codeParam == None:
        return "Bro, you're buggin..."
    global youtube_access_token 
    youtube_access_token = youtubeAuth.callback(codeParam)
    return redirect('/YoutubeAuthed')

@app.route('/YoutubeAuthed')
def youtubeAuthed():
    return "Nice, authed."

if __name__ == "__main__":
    app.run(debug=True)