from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.database import Base

class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(String, primary_key=True, index=True)  # Spotify URI
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(String, nullable=False)
    songs_count = Column(Integer, nullable=False)
    followers_count = Column(Integer, nullable=False)

    categories = relationship(
        "CategoryPlaylist",
        back_populates="playlist",
    )

    songs = relationship(
        "SongPlaylist",
        back_populates = "playlist",
    )
