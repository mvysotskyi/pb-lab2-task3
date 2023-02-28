"""
Module contains functions to work with Spotify API.
"""

import base64
import requests

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
    url = "https://api.spotify.com/v1/search"

    response = requests.get(
        url,
        params={"q": artist, "type": "artist"},
        headers={"Authorization": "Bearer " + token},
        timeout=10
    )

    result = response.json()

    if "artists" not in result:
        return None

    if len(result["artists"]["items"]) == 0:
        return None

    return result["artists"]["items"][0]["id"]

def get_artist_top_track(token: str, artist_id: str, market: str = "US") -> list[str]:
    """
    Get artist top track id.
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market={market}"

    response = requests.get(
        url,
        headers={"Authorization": "Bearer " + token},
        timeout=10
    )

    result = response.json()

    if "tracks" not in result:
        return None

    if len(result["tracks"]) == 0:
        return None

    return result["tracks"][0]["name"]

def get_available_markets(token: str) -> list[str]:
    """
    Tracks markets from Spotify API.
    """
    url = "https://api.spotify.com/v1/markets"

    response = requests.get(
        url,
        headers={"Authorization": "Bearer " + token},
        timeout=10
    )

    result = response.json()
    return result["markets"] if "markets" in result else []
