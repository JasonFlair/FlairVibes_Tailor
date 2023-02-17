#!/usr/bin/python3
"""file used for tests and planning should not be expected to work
    as a lot here is pseudocode and stuff being worked out"""

from flask import Flask, request, abort
import requests

app = Flask(__name__)

@app.route('/submit', methods=['POST'], strict_slashes=False)
def submit_song():
    """gets the song details from user and works using the details"""

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
    song_name = data.get('song_name')
    artist = data.get('artist')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"}
    search_song_url = f"https://api.spotify.com/v1/search?q={song_name}+ artist:{artist}&type=track"

    """song_name = input("Enter song name: ").replace(".", "")
    artist = input("Enter artist name: ")
    print()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {bearer token}"}
    search_song_url = f"https://api.spotify.com/v1/search?q={song_name}+ artist:{artist}&type=track"
    """
    response = requests.get(search_song_url, headers=headers)
    json_resp = response.json()
    track_id = json_resp['tracks']['items'][0]['id']
    artist_id = json_resp['tracks']['items'][0]['album']['artists'][0]['id']
    print(artist_id)
    """print(track_id)
    print()
    print(artist_id)
    print()"""
    search_features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    features_response = requests.get(search_features_url, headers=headers)
    features_json = features_response.json()
    danceability = features_json['danceability']
    tempo = features_json['tempo']
    key = features_json['key']

    """print(f"here are the audio features of {song_name}:")
    print(f"danceability: {danceability}")
    print(f"liveness: {liveness}")
    print(f"tempo: {tempo}")
    print(f"key: {key}")"""

    recommendations = get_recommendations(danceability, tempo, key, track_id, artist_id, song_name)
    return recommendations

def get_recommendations(danceability, tempo, key, track_id, artist_id, song_name):

    """gets recommendations based on parameters passed"""
    headers = { "Authorization": "Authorization"}

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
    return recommended_tracks_json




if __name__ == "__main__":
    submit_song()
    app.run(host='0.0.0.0', port=5000)