from sqlalchemy import Column, String, Integer
from app.database import Base

class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(String, primary_key=True, index=True)  # Spotify URI
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(String, nullable=False)
    songs_count = Column(Integer, nullable=False)
    followers_count = Column(Integer, nullable=False)
