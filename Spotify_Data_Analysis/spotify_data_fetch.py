import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

CLIENT_ID = "PUT YOUR OWN KEYS"
CLIENT_SECRET = "PUT YOUR OWN KEYS"

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def fetch_artist_data(artist_name):
    results = sp.search(q=artist_name, type="artist", limit=1)
    if not results['artists']['items']:
        print("Artist not found!")
        return
    artist = results['artists']['items'][0]
    artist_data = {
        "Name": artist['name'],
        "Followers": artist['followers']['total'],
        "Genres": ", ".join(artist['genres']),
        "Popularity": artist['popularity']
    }
    df = pd.DataFrame([artist_data])
    df.to_csv('data/artists.csv', index=False)
    print("Artist data saved to data/artists.csv")

def fetch_album_data(artist_name):
    results = sp.search(q=artist_name, type="artist", limit=1)
    if not results['artists']['items']:
        print("Artist not found!")
        return
    artist_id = results['artists']['items'][0]['id']
    
    album_data = []
    offset = 0
    while True:
        albums = sp.artist_albums(artist_id, album_type='album', limit=50, offset=offset)
        if not albums['items']:
            break
        for album in albums['items']:
            album_data.append({
                "Name": album['name'],
                "Release Date": album['release_date'],
                "Total Tracks": album['total_tracks'],
                "Album Type": album['album_type']
            })
        offset += 50

    df = pd.DataFrame(album_data)
    df.to_csv('data/albums.csv', index=False)
    print("Album data saved to data/albums.csv")

def fetch_all_tracks_data(artist_name):
    results = sp.search(q=artist_name, type="artist", limit=1)
    if not results['artists']['items']:
        print("Artist not found!")
        return
    artist_id = results['artists']['items'][0]['id']
    
    
    album_data = []
    offset = 0
    while True:
        albums = sp.artist_albums(artist_id, album_type='album', limit=50, offset=offset)
        if not albums['items']:
            break
        album_data.extend(albums['items'])
        offset += 50

   
    track_data = []
    for album in album_data:
        tracks = sp.album_tracks(album['id'])
        for track in tracks['items']:
            track_data.append({
                "Track Name": track['name'],
                "Album Name": album['name'],
                "Duration (ms)": track['duration_ms'],
                "Explicit": track['explicit'],
                "Track Number": track['track_number']
            })

    df = pd.DataFrame(track_data)
    df.to_csv('data/all_tracks.csv', index=False)
    print("All tracks data saved to data/all_tracks.csv")


if __name__ == "__main__":
    artist_name = input("Enter the artist's name: ")
    fetch_artist_data(artist_name)
    fetch_album_data(artist_name)
    fetch_all_tracks_data(artist_name)
