#!/usr/bin/python3

"""file used for tests and planning"""
from flask import Flask, request, abort
import requests

app = Flask(__name__)

@app.route('/submit', methods=['POST'], strict_slashes=False)
def submit_song():
    """gets the song details from user and works using the details"""
    song_name = input("Enter song name: ").replace(".", "")
    artist = input("Enter artist name: ")
    print()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer BQD_bPQ2H-U9JK2pD876Sy5ZTcmbLpsjfmIS10Vdhe4pJdpazIwTNIRIiRBySu3U_klAvITz4GO3Wk1AxJrAMzp3uE_B0JVK5NV0CDxwEXT-Xt62jHQ7zmkSR74pUB_FpDBi_9Yp7Z96yZxmzPVv4eb3FyHKG97njo4uzfhYqSdR8fDMt2LG8_bWHUlwYcLzx-ig"}
    search_song_url = f"https://api.spotify.com/v1/search?q={song_name}+ artist:{artist}&type=track"
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
    headers = { "Authorization": "Bearer BQAitfSE5IDoDF8xY6AVDchUIArNB2qo7m1PVAZ5Hg-uqmg2_rqQB4tTL3p-ZdGYw0-L3gBbZLIBnqMKOKjvCFNfeIjuyrk3fV6MEkMTL-GyAH_JNYAMek0VQFnsywQkLbjghrzqsjRh0Cn7PwtO-kelc8MzcVifXiZnMd5aLD60ZTHEdjI-eWGROZcsBb8vfuA1"}

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