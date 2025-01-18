from pydantic import BaseModel
from typing import List

class TrackDTO(BaseModel):
    id: str
    name: str
    image_url: str | None
    artist_name: str
    artist_id: str
    duration: int


class PlaylistDTO(BaseModel):
    id: str
    name: str
    image_url: str | None
    description: str
    songs_count: int
    followers_count: int
    tracks: List[TrackDTO]
    categories: List[str]