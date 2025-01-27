#there is used psycopg2, because I had problems with inserting by using sqlalchemy
import psycopg2
from psycopg2.extras import execute_batch
from typing import List
import os
from dotenv import load_dotenv
from pathlib import Path
from spoitify_utils import fetch_playlists_data
from spotify_models import PlaylistDTO

dotenv_path = Path('./.env')
load_dotenv()
DB_PASSWORD = os.getenv('DB_PASSWORD')

def save_to_database(playlists: List[PlaylistDTO]):
    # Database connection configuration
    conn = psycopg2.connect(
        dbname="playlisearch",
        user="postgres",
        password=DB_PASSWORD,
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    try:
        # Insert categories
        category_query = """
            INSERT INTO "categories" ("name")
            VALUES (%s)
            ON CONFLICT ("name") DO NOTHING;
        """
        categories = {category for playlist in playlists for category in playlist.categories}
        execute_batch(cursor, category_query, [(category,) for category in categories])

        # Insert playlists
        playlist_query = """
            INSERT INTO "playlists" ("id", "name", "image_url", "description", "songs_count", "followers_count")
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT ("id") DO NOTHING;
        """
        execute_batch(cursor, playlist_query, [
            (playlist.id, playlist.name, playlist.image_url, playlist.description, playlist.songs_count, playlist.followers_count)
            for playlist in playlists
        ])

        # Insert songs
        song_query = """
            INSERT INTO "songs" ("id", "name", "image_url", "artist_name", "artist_id", "duration")
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT ("id") DO NOTHING;
        """
        songs = {
            (track.id, track.name, track.image_url, track.artist_name, track.artist_id, track.duration)
            for playlist in playlists for track in playlist.tracks
        }
        execute_batch(cursor, song_query, list(songs))

        # Insert categories_playlists relationships
        categories_playlists_query = """
            INSERT INTO "categories_playlists" ("category_id", "playlist_id")
            VALUES ((SELECT "id" FROM "categories" WHERE "name" = %s), %s)
            ON CONFLICT ("category_id", "playlist_id") DO NOTHING;
        """
        categories_playlists = [
            (category, playlist.id)
            for playlist in playlists for category in playlist.categories
        ]
        execute_batch(cursor, categories_playlists_query, categories_playlists)

        # Insert songs_playlists relationships
        songs_playlists_query = """
            INSERT INTO "songs_playlists" ("song_id", "playlist_id")
            VALUES (%s, %s)
            ON CONFLICT ("song_id", "playlist_id") DO NOTHING;
        """
        songs_playlists = [
            (track.id, playlist.id)
            for playlist in playlists for track in playlist.tracks
        ]
        execute_batch(cursor, songs_playlists_query, songs_playlists)

        # Commit the transaction
        conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
    keyword = 'favourites' #change this manually
    amount = 100
    save_to_database((fetch_playlists_data(keyword, amount)))