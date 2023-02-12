#!/usr/bin/python3
from flask import Flask
import requests

app = Flask(__name__)

def submit_song():
    """gets the song details from user and works using the details"""
    song_name = input("Enter song name: ").replace(".", "")
    artist = input("Enter artist name: ")
    print()
    headers = {
        "Authorization": "Bearer BQCEGwHr7B8ISalWrK27Al-Z_pOAyTNN7bDkX8mBRLr66sQXXWeErceeSpxzBBZiGRHhI54AWH5TlW27oXdMRMPYDVhI34I8MhtRrVJpLIUqgLiKViQj1U3rBeB1Cd_G9yAqTNzrNTS4MaHAcpmYA5g6aAR9wOrIh-gZ-8Batrc4Bcl90-SkBfQ1c7XIvhzAVppC"}
    search_song_url = f"https://api.spotify.com/v1/search?q={song_name}+ artist:{artist}&type=track"
    response = requests.get(search_song_url, headers=headers)
    json_resp = response.json()
    track_id = json_resp['tracks']['items'][0]['id']
    artist_id = json_resp['tracks']['items'][0]['album']['artists'][0]['id']
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

    get_recommendations(danceability, tempo, key, track_id, artist_id, song_name)

def get_recommendations(danceability, tempo, key, track_id, artist_id, song_name):

    """gets recommendations based on parameters passed"""
    headers = { "Authorization": "Bearer BQCEGwHr7B8ISalWrK27Al-Z_pOAyTNN7bDkX8mBRLr66sQXXWeErceeSpxzBBZiGRHhI54AWH5TlW27oXdMRMPYDVhI34I8MhtRrVJpLIUqgLiKViQj1U3rBeB1Cd_G9yAqTNzrNTS4MaHAcpmYA5g6aAR9wOrIh-gZ-8Batrc4Bcl90-SkBfQ1c7XIvhzAVppC"}

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
    for track in recommendations_json['tracks']:
        artist = track['artists'][0]['name']
        track_title = track['name']
        track_title = track_title.replace(".", "")
        if track_title.lower() != song_name.lower():
            print(f"{track_title} by {artist}")




if __name__ == "__main__":
    submit_song()