"""
Module docstring.
"""

import json

from flask import Flask, render_template
from flask import request

from map_creator import create_map, read_countries_dataset
from spotify_api import *

app = Flask(__name__, static_folder='static', template_folder='templates')

CLIENT_ID = "682a8d68a9904c2290cbce40adf8e2e0"
CLIENT_SECRET = "8c250c51eab4438c99f5c849d68d4d3b"

@app.route('/')
def index():
    """
    Main page rendering.
    """
    return render_template('index.html')

@app.route('/map-placeholder')
def map_placeholder():
    """
    Just render template with map placeholder.
    """
    return render_template('map-placeholder.html')

@app.post('/map')
def map_page():
    """
    Function docstring.
    """
    token = get_token(CLIENT_ID, CLIENT_SECRET)

    available_markets = get_available_markets(token)
    countries = read_countries_dataset('countries.csv')

    if not available_markets:
        return json.dumps({"status": 404, "content" : "No available markets."})

    artist = request.form['artist']
    artist_id = get_artist_id(token, artist)

    if not artist_id:
        return json.dumps({"status": 404, "content" : "No artist found."})

    points = []
    for market in available_markets:
        top_track = get_artist_top_track(token, artist_id, market=market)
        if not top_track:
            continue

        if market in countries:
            points.append((countries[market][0], countries[market][1], top_track))

    world_map = create_map(points)
    return json.dumps({"status": 200, "content": world_map._repr_html_()})

if __name__ == '__main__':
    app.run(debug=True)
