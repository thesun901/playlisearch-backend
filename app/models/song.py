from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from app.database import Base

class Song(Base):
    __tablename__ = "songs"
    id = Column(String, primary_key=True)  # Text ID (Spotify URI)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    artist_name = Column(String, nullable=False)
    artist_id = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in milliseconds

    # Relationship to associate songs with playlists
    playlists = relationship("SongPlaylist", back_populates="song")