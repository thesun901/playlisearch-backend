from collections import Counter
from typing import List, Dict

import spotipy
import os
from dotenv import load_dotenv
from pathlib import Path
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from app.utils.spotify_models import PlaylistDTO, TrackDTO
import json


dotenv_path = Path('./.env')
load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

scope = "user-library-read"
sp_oauth = SpotifyOAuth(
     client_id=CLIENT_ID,
     client_secret=CLIENT_SECRET,
     redirect_uri='http://localhost:3000',
     scope=scope,
     show_dialog=True
 )
sp = spotipy.Spotify(auth_manager=sp_oauth)


CACHE_FILE = Path("artist_cache.json")

artist_cache: Dict[str, List[str]] = {}

def categorize_playlist(playlist_tracks: List[dict]) -> List[str]:
    category_counter = Counter()

    for track_item in playlist_tracks:
        track = track_item.get('track')
        if track and 'episode' in track.keys() and not track['episode']:
            artist_id = track['artists'][0]['id']
            artist_categories = fetch_artist_categories(artist_id)
            category_counter.update(artist_categories)

    print(category_counter)
    # Get the top 6 most common categories
    top_categories = [category for category, _ in category_counter.most_common(6)]
    return top_categories


def load_cache():
    global artist_cache
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r") as file:
            artist_cache = json.load(file)
    else:
        artist_cache = {}

def save_cache():
    with open(CACHE_FILE, "w") as file:
        json.dump(artist_cache, file, indent=4)

def fetch_artist_categories(artist_id: str) -> List[str]:
    if artist_id in artist_cache:
        return artist_cache[artist_id]  # Return cached categories

    # Simulate fetching artist categories from Spotify API
    # Replace this with actual API call if available
    categories = sp.artist(artist_id)['genres']
    artist_cache[artist_id] = categories
    save_cache()
    return categories


def fetch_playlists_data(phrase: str, amount: int) -> List[PlaylistDTO]:
    load_cache()
    items = []
    result = sp.search(q=phrase, type='playlist', limit=amount if amount <= 50 else 50)

    #for some reason spotify generated playlists are classified as none, but that is good since we don't want them
    playlists = [playlist for playlist in result['playlists']['items'] if playlist is not None]

    while amount > len(items) and result['playlists']['next']:
        for playlist in playlists:
            playlist_tracks = sp.playlist_items(playlist['id'])['items']
            tracks = []

            for track_item in playlist_tracks:
                track = track_item['track']
                if track is not None and not 'episode' not in track.keys() and 'album' in track.keys():
                    tracks.append(TrackDTO(
                        id=track['id'],
                        name=track['name'],
                        image_url=track['album']['images'][0]['url'] if 'images' in track['album'].keys() else None,
                        artist_name=track['artists'][0]['name'],
                        artist_id=track['artists'][0]['id'],
                        duration=track['duration_ms']
                    ))


            categories = categorize_playlist(playlist_tracks)

            items.append(PlaylistDTO(
                id=playlist['id'],
                name=playlist['name'],
                image_url=playlist['images'][0]['url'] if playlist['images'] else None,
                description=playlist.get('description', ''),
                songs_count=playlist['tracks']['total'],
                followers_count=playlist.get('followers', {}).get('total', 0),
                tracks=tracks,
                categories=categories
            ))

        result = sp.next(result['playlists'])

    return items

if __name__ == '__main__':
    fetch_playlists_data('cool', 100)
