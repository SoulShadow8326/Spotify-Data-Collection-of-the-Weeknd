import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = '58dbaea9e05d494ba5d03e2cc0303669'
CLIENT_SECRET = '1b0aa3e7702f4919bcc425ccd849d83e'

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

artist_name = "The Weeknd"
results = sp.search(q=artist_name, type='artist', limit=1)
artist_id = results['artists']['items'][0]['id']

target_genres = ["canadian pop", "pop", "canadian contemporary r&b"]

albums = sp.artist_albums(artist_id, album_type='album', country='US', limit=50)
album_ids = [album['id'] for album in albums['items']]

all_tracks = []
for album_id in album_ids:
    tracks = sp.album_tracks(album_id)
    for track in tracks['items']:
        all_tracks.append({
            'track_name': track['name'],
            'album_name': sp.album(album_id)['name'],
            'release_date': sp.album(album_id)['release_date']
        })


import random  

songs_by_genre = {genre: [] for genre in target_genres}
for track in all_tracks:
    
    genre = random.choice(target_genres)
    if len(songs_by_genre[genre]) < 7:  
        songs_by_genre[genre].append(f"{track['track_name']} (Album: {track['album_name']}, Released: {track['release_date']})")


output_file = "the_weeknd_diverse_songs_by_genre.txt"
with open(output_file, "w") as f:
    for genre, songs in songs_by_genre.items():
        f.write(f"--- {genre.upper()} ---\n")
        for song in songs:
            f.write(f"{song}\n")
        f.write("\n")

print(f"File '{output_file}' created successfully.")
