from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class CategoryPlaylist(Base):
    __tablename__ = "categories_playlists"

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    playlist_id = Column(String, ForeignKey("playlists.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    category = relationship("Category", back_populates="playlists")
    playlist = relationship("Playlist", back_populates="categories")
