import logging
from collections import Counter

from fastapi import FastAPI, Depends, Query
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from typing import List, Dict
from app.database import SessionLocal
from app.models import Playlist, Category, CategoryPlaylist, SongPlaylist
from app.utils.spoitify_utils import fetch_artist_categories

app = FastAPI()

logger = logging.getLogger(__name__)

def get_db():
    db_obj = SessionLocal()
    db = db_obj()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        try:
            db.close()
        except Exception as close_error:
            logger.error(f"Error closing database session: {close_error}")

@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI app!"}

@app.get("/playlists")
def get_playlists_by_categories(
    categories: List[str] = Query(...),
    amount: int = Query(5, ge=1),
    db: Session = Depends(get_db)
):
    try:
        # Query playlists with their categories and songs
        playlists = (
            db.query(Playlist)
            .join(CategoryPlaylist, Playlist.id == CategoryPlaylist.playlist_id)
            .join(Category, CategoryPlaylist.category_id == Category.id)
            .options(
                joinedload(Playlist.songs).joinedload(SongPlaylist.song)  # Load songs associated with each playlist
            )
            .filter(Category.name.in_(categories))
            .order_by(func.random())  # Randomize the order of results
            .limit(amount)
            .all()
        )

        # Map playlist IDs to their associated categories and songs
        playlist_category_map: Dict[str, List[str]] = {}
        playlist_songs_map: Dict[str, List[Dict]] = {}

        for playlist in playlists:
            # Collect categories for each playlist
            playlist_category_map[playlist.id] = [
                category.category.name for category in playlist.categories
            ]

            # Collect songs for each playlist
            playlist_songs_map[playlist.id] = [
                {
                    "id": song_playlist.song.id,
                    "name": song_playlist.song.name,
                    "image_url": song_playlist.song.image_url,
                    "artist_name": song_playlist.song.artist_name,
                    "artist_id": song_playlist.song.artist_id,
                    "duration": song_playlist.song.duration,
                }
                for song_playlist in playlist.songs
            ]

        # Format the response
        result = [
            {
                "id": playlist.id,
                "name": playlist.name,
                "image_url": playlist.image_url,
                "description": playlist.description,
                "songs_count": playlist.songs_count,
                "followers_count": playlist.followers_count,
                "categories": playlist_category_map.get(playlist.id, []),
                "songs": playlist_songs_map.get(playlist.id, []),
            }
            for playlist in playlists
        ]

        return {"playlists": result}

    except Exception as e:
        return {"error": str(e)}


@app.get("/top-categories")
def get_top_categories(
    artist_ids: List[str] = Query(..., description="List of artist IDs"),
):
    try:

        category_counter = Counter()

        # Fetch categories for each artist
        for artist_id in artist_ids:
            artist_categories = fetch_artist_categories(artist_id)
            category_counter.update(artist_categories)

        # Get the top 10 most common categories
        top_categories = [
            {"category": category, "count": count}
            for category, count in category_counter.most_common(10)
        ]

        return {"top_categories": top_categories}

    except Exception as e:
        return {"error": str(e)}