import sys
from flask import Flask, render_template, url_for, redirect, request, make_response, session
sys.path.insert(1, 'serverCode')
from serverCode import spotifyAuth, youtubeAuth, apiKeys

app = Flask(__name__)
spotify_access_token = ''
youtube_credentials = None
app.secret_key = apiKeys.flask_session_secret_key

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
        playlistInfoArray = spotifyAuth.getTracks(spotify_access_token, selectedPlaylist)
        return render_template('spotifyTracksView.html', playlistInfoArray=playlistInfoArray)

@app.route('/YoutubeLogin', methods=['GET', 'POST'])
def youtubeLogin():
    if request.method == 'POST':
        session[spotify_access_token] = request.form.getlist('tracks')
    return redirect(youtubeAuth.auth())

@app.route('/YoutubeCallback')
def youtubeCallback():
    codeParam = request.url
    # Also check if state has changed as well later
    if codeParam == None:
        return "Bro, you're buggin..."
    global youtube_credentials
    youtube_credentials = youtubeAuth.callback(codeParam)
    return redirect('/YoutubeAuthed')

@app.route('/YoutubeAuthed')
def youtubeAuthed():
    create_playlist_response = youtubeAuth.makePlaylist(youtube_credentials)
    playlistID = create_playlist_response['id']
    return render_template('youtubeFromSpotify.html', playlistId=playlistID)

@app.route('/YTPlaylistDelete/<playlistID>')
def ytPlaylistDelete(playlistID):
    youtubeAuth.deletePlaylist(youtube_credentials, playlistID)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)