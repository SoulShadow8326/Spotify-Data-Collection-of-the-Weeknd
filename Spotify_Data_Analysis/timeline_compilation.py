import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

CLIENT_ID = "PUT YOUR OWN KEYS"
CLIENT_SECRET = "PUT YOUR OWN KEYS"

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

artist_name = "The Weeknd"
results = sp.search(q=artist_name, type='artist', limit=1)
artist_id = results['artists']['items'][0]['id']

albums = sp.artist_albums(artist_id, album_type='album', limit=50)
album_data = []
for album in albums['items']:
    album_data.append({
        'Album Name': album['name'],
        'Release Date': album['release_date'],
        'Album ID': album['id']
    })

albums_df = pd.DataFrame(album_data)
albums_df['Release Date'] = pd.to_datetime(albums_df['Release Date'])

track_data = []
for album_id in albums_df['Album ID']:
    tracks = sp.album_tracks(album_id)
    for track in tracks['items']:
        track_data.append({
            'Track Name': track['name'],
            'Album Name': albums_df.loc[albums_df['Album ID'] == album_id, 'Album Name'].values[0],
            'Release Date': albums_df.loc[albums_df['Album ID'] == album_id, 'Release Date'].values[0]
        })

tracks_df = pd.DataFrame(track_data)

albums_df.drop(columns=['Album ID']).to_csv("the_weeknd_albums.csv", index=False)
tracks_df.to_csv("the_weeknd_tracks.csv", index=False)

plt.figure(figsize=(12, 6))
for _, row in albums_df.iterrows():
    plt.plot([row['Release Date'], row['Release Date']], [0, 1], color='gray', linestyle='--', alpha=0.6)
    plt.scatter(row['Release Date'], 1, color='blue', label='Album Release')
    plt.text(row['Release Date'], 1.05, row['Album Name'], rotation=45, fontsize=8, ha='right')

for _, row in tracks_df.iterrows():
    plt.plot([row['Release Date'], row['Release Date']], [0, 0.5], color='gray', linestyle='--', alpha=0.4)
    plt.scatter(row['Release Date'], 0.5, color='green', label='Track Release' if _ == 0 else "")

plt.title("The Weeknd: Albums and Tracks Timeline", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.yticks([0.5, 1], ["Tracks", "Albums"])
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()

plt.savefig("the_weeknd_timeline.png", transparent=True)
plt.show()
