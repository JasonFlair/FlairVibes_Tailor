if __name__ == '__main__':
    import requests
    headers = {"Authorization": "Bearer BQABJUo6ejIIhG1vq3gvJ8OvNlei2njqwTW3USey4uEaQ_CwM0yLFYw-lPRmQA4MPyafzTRN7zNrV17EtIfniFwZ80T95id96rwnD7RaAAET-6RwmXjMl_XzWmTasfGnMcPrgDVuOSFfwbhKDEzH0a4we_U30PHEYturPm6Msy-yC1YYQfCiD9KPzgUxDC_On1FN"}
    url = f"https://api.spotify.com/v1/search?q={'arcadia'}+ artist:{'lana del rey'}&type=track"
    response = requests.get(url, headers=headers)
    json_resp = response.json()
    track_id = json_resp['tracks']['items'][0]['id']
    print(track_id)

