"""
Module contains functions to work with Spotify API.
"""

import base64
import requests

CLIENT_ID = "682a8d68a9904c2290cbce40adf8e2e0"
CLIENT_SECRET = "8c250c51eab4438c99f5c849d68d4d3b"

def get_token(client_id: str, client_secret: str) -> str:
    """
    Get token from Spotify API.
    """
    url = "https://accounts.spotify.com/api/token"
    auth_base64 = str(base64.b64encode((client_id + ":" + client_secret).encode("utf-8")), "utf-8")
    data = {"grant_type": "client_credentials"}

    response = requests.post(
        url,
        data=data,
        headers={"Authorization": "Basic " + auth_base64},
        timeout=10
    )

    result = response.json()
    return result["access_token"] if "access_token" in result else None

def get_artist_id(token: str, artist: str) -> str:
    """
    Get artist id from Spotify API.
    """
    url = f"https://api.spotify.com/v1/search?q=artist:{artist}&type=artist"

    response = requests.get(
        url,
        headers={"Authorization": "Bearer " + token},
        timeout=10
    )

    result = response.json()

    if len(result["artists"]["items"]) == 0:
        return None

    return result["artists"]["items"][0]["id"] if "artists" in result else None

def get_artist_top_track_id(token: str, artist_id: str) -> list[str]:
    """
    Get artist top track id.
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"

    response = requests.get(
        url,
        headers={"Authorization": "Bearer " + token},
        timeout=10
    )

    result = response.json()

    if len(result["tracks"]) == 0:
        return None

    return result["tracks"][0]["id"] if "tracks" in result else None

def get_available_markets(token: str, track_id: str) -> list[str]:
    """
    Tracks markets from Spotify API.
    """
    url = f"https://api.spotify.com/v1/tracks/{track_id}"

    response = requests.get(
        url,
        headers={"Authorization": "Bearer " + token},
        timeout=10
    )

    result = response.json()
    return result["available_markets"] if "available_markets" in result else None
