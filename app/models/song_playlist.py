from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SongPlaylist(Base):
    __tablename__ = "songs_playlists"

    song_id = Column(String, ForeignKey("songs.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    playlist_id = Column(String, ForeignKey("playlists.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    song = relationship("Song", back_populates="playlists")
    playlist = relationship("Playlist", back_populates="songs")
