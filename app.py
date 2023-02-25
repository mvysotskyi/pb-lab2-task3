"""
Module docstring.
"""

import json

from flask import Flask, render_template
from flask import request

from map_creator import create_map, read_countries_dataset
from spotify_api import get_token, get_artist_id, get_artist_top_track_id, get_available_markets

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
    print(request.form)
    artist = request.form['artist']
    token = get_token(CLIENT_ID, CLIENT_SECRET)

    artist_id = get_artist_id(token, artist)

    if not artist_id:
        return json.dumps({"status": 404, "content" : "No artist found."})

    track_id = get_artist_top_track_id(token, artist_id)
    available_markets = get_available_markets(token, track_id)

    if not available_markets:
        return json.dumps({"status": 404, "content" : "No available markets for this artist."})

    countries = read_countries_dataset('countries.csv')

    points = []
    for country, location in countries.items():
        if country in available_markets:
            points.append(location)

    world_map = create_map(points)
    return json.dumps({"status": 200, "content": world_map._repr_html_()})

if __name__ == '__main__':
    app.run(debug=True)
