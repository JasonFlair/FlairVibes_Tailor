#!/usr/bin/python3
"""submits song of the user's choice and
    recommends songs based on similarity"""

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import requests

app = Flask(__name__)
cors = CORS(app)

@app.route('/submit_song', methods=['POST'])
def submit_song():
    # Get the data from the POST request
    if request.get_json() is None:
        abort(400, "Not a json")
    data = request.get_json()
    song_name = data.get('song_name')
    artist = data.get('artist')
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {bearer token}"}
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

    print(f"based on your favourite song, {song_name}, here are some songs we think you might like:")
    print()
    recommended_tracks = []
    for track in recommendations_json['tracks']:
        artist = track['artists'][0]['name']
        track_title = track['name']
        track_title = track_title.replace(".", "")
        if track_title.lower() != song_name.lower():
            recommended_tracks.append(f"{track_title} by {artist}")
    recommended_tracks_json = {"tracks": recommended_tracks}
    # Return the recommendations response from spotify
    return jsonify(recommended_tracks_json)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)