import sys
from flask import Flask, render_template, url_for, redirect
sys.path.insert(1, 'serverCode')
from serverCode import spotifyAuth

app = Flask(__name__)

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
    return redirect(spotifyAuth.auth(1, 1))

@app.route('/SpotifyCallback')
def spotifyCallback():
    return "Succesfully logged in!"

if __name__ == "__main__":
    app.run(debug=True)