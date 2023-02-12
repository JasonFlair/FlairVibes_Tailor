if __name__ == '__main__':
    import requests
    headers = {"Authorization": "Bearer BQABJUo6ejIIhG1vq3gvJ8OvNlei2njqwTW3USey4uEaQ_CwM0yLFYw-lPRmQA4MPyafzTRN7zNrV17EtIfniFwZ80T95id96rwnD7RaAAET-6RwmXjMl_XzWmTasfGnMcPrgDVuOSFfwbhKDEzH0a4we_U30PHEYturPm6Msy-yC1YYQfCiD9KPzgUxDC_On1FN"}
    url = f"https://api.spotify.com/v1/search?q={'arcadia'}+ artist:{'lana del rey'}&type=track"
    response = requests.get(url, headers=headers)
    json_resp = response.json()
    print(json_resp)
    track_id = json_resp['tracks']['items'][0]['id']
    print(track_id)

from flask import Flask
import requests
import pandas as pd
from sklearn.mixture import GaussianMixture

app = Flask(__name__)



import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture

# Load the audio features data into a pandas DataFrame
df = pd.read_csv("audio_features.csv")

# Preprocess the data (if necessary)
# ...

# Train the GaussianMixture model on the audio features
X = df[["danceability", "liveness", "tempo", "key"]].values
gmm = GaussianMixture(n_components=10)
gmm.fit(X)

# Find the audio features of the input song
input_song = np.array([[0.721, 0.341, 124.02, 7]])

# Calculate the likelihood of the input song under each Gaussian distribution
probs = gmm.predict_proba(input_song)

# Find the indices of the songs with the highest probabilities
indices = np.argmax(probs, axis=1)

# Select the top k songs with the highest probabilities
k = 5
top_k = df.iloc[indices][:k]

# Print the top k songs
print("Top %d similar songs:" % k)
for i, row in top_k.iterrows():
    print("- Song: %s" % row["song_id"])
    print("  Danceability: %.3f" % row["danceability"])
    print("  Liveness: %.3f" % row["liveness"])
    print("  Tempo: %.2f" % row["tempo"])
    print("  Key: %d" % row["key"])


def submit_song():
    """gets the song details from user and works using the details"""
    song_name = input("Enter song name: ")
    artist = input("Enter artist name: ")
    headers = {
        "Authorization": "Bearer BQDW5fiDeEC1jEPhaZgDdBJtgKd-8t63Nv1mZ6tsggeiPra0q"
                         "rRXhiGbBj2S7uL73ToiynkwZL_lX96xlQDEdzdtUVPB5e0Q40S58siTGFNd7K4o4iw3KeimWVxq"
                         "jwpE1QIw3givzx7xXzKIypgkxUPCgN7V_W4x1jeKknOLRPw"
                         "drM9mYbUSuS1UfMKV8OQsCttx"}
    search_song_url = f"https://api.spotify.com/v1/search?q={song_name}+ artist:{artist}&type=track"
    response = requests.get(search_song_url, headers=headers)
    json_resp = response.json()
    track_id = json_resp['tracks']['items'][0]['id']
    search_features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    features_response = requests.get(search_features_url, headers=headers)
    features_json = features_response.json()
    danceability = features_json['danceability']
    tempo = features_json['tempo']
    liveness = features_json['liveness']
    key = features_json['key']

    submitted_song_features = [danceability, liveness, tempo, key]

    # Load the dataset of audio features
    dataset = pd.read_csv("audio_features.csv")

    # Select the columns you want to use for building the GaussianMixture model
    X = dataset[['danceability', 'liveness', 'tempo', 'key']]

    # Train the GaussianMixture model
    gmm = GaussianMixture(n_components=10)
    gmm.fit(X)

    # Use the GaussianMixture model to predict the similarity of the submitted song to the songs in the dataset
    similarity_scores = gmm.score_samples([submitted_song_features])

    # Get the indices of the top 5 most similar songs
    top_5_indices = similarity_scores.argsort()[-5:][::-1]

    # Print the details of the top 5 most similar songs
    print


