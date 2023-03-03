#!/usr/bin/python3
"""submits song of the user's choice and
    recommends songs based on similarity"""

from dynamic_webf.api import fvt_views
import base64
from flask import request, jsonify, abort
from os import getenv
import requests


@fvt_views.route('/submit_song', methods=['POST'], strict_slashes=False)
def submit_song():
    """an end point that receives submitted songs and then gets audio info for those songs
        and then makes requests to spotify's recommendations endpoint"""

    # get an access token whenever a user uses the service using client id and secret
    client_id = getenv("CLIENT_ID")
    client_secret = getenv("CLIENT_SECRET")

    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8"))
    # make request to spotify api to get an access token
    token_resp = requests.post("https://accounts.spotify.com/api/token",
                             headers={"Authorization": f"Basic {auth_header.decode('utf-8')}"},
                             data={"grant_type": "client_credentials"})
    access_token = token_resp.json()['access_token']


    # Get the data from the POST request
    if request.get_json() is None:
        abort(400, "Not a json")
    data = request.get_json()
    song_name = data.get('song_name').replace(".", "").replace("?", "").strip()
    artist = data.get('artist')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"}
    search_song_url = f"https://api.spotify.com/v1/search?q={song_name}+ artist:{artist}&type=track"

    # Make the GET request to spotify
    spotify_response = requests.get(search_song_url, headers=headers)
    spotify_response_json = spotify_response.json()
    track_id = spotify_response_json['tracks']['items'][0]['id']
    artist_id = spotify_response_json['tracks']['items'][0]['album']['artists'][0]['id']
    search_features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    features_response = requests.get(search_features_url, headers=headers)
    features_json = features_response.json()

    # audio features to be used
    danceability = features_json['danceability']
    tempo = features_json['tempo']
    key = features_json['key']

    # audio features query parameters tuned
    min_danceability = danceability - 0.031
    max_danceability = danceability + 0.3
    min_tempo = tempo - 4
    max_tempo = tempo + 10
    min_key = key - 1
    max_key = key + 3
    min_popularity = 15
    max_popularity = 100

    recommendations_url = f"https://api.spotify.com/v1/recommendations?limit=10&seed_artists={artist_id}&seed_tracks={track_id}" \
                          f"&min_danceability={min_danceability}&max_danceability={max_danceability}&min_key={min_key}" \
                          f"&max_key={max_key}&min_popularity={min_popularity}&max_popularity={max_popularity}&min_tempo={min_tempo}&max_tempo={max_tempo}"

    recommendations_resp = requests.get(recommendations_url, headers=headers)
    recommendations_json = recommendations_resp.json()

    recommended_tracks = []
    for track in recommendations_json['tracks']:
        artist = track['artists'][0]['name']
        track_title = track['name']
        track_title = track_title.replace(".", "").replace("?", "")
        track_link = track['external_urls']['spotify']
        rec_track_id = track['id']
        if track_title.lower() != song_name.lower():
            recommended_tracks.append(f'{{"title": "{track_title}", "artist": "{artist}", "link": "{track_link}", "id": "{rec_track_id}"}}')
    recommended_tracks_json = {"tracks": recommended_tracks}
    # Return the recommendations response from spotify
    return jsonify(recommended_tracks_json)

