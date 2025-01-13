"""Create tables

Revision ID: abc12345
Revises:
Create Date: 2025-01-13

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'abc12345'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create Categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
    )

    # Create Playlists table
    op.create_table(
        'playlists',
        sa.Column('id', sa.String, primary_key=True),  # Spotify URI
        sa.Column('name', sa.String, nullable=False),
        sa.Column('image_url', sa.String, nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('songs_count', sa.Integer, nullable=False),
        sa.Column('followers_count', sa.Integer, nullable=False),
    )

    # Create Songs table
    op.create_table(
        'songs',
        sa.Column('id', sa.String, primary_key=True),  # Spotify URI
        sa.Column('name', sa.String, nullable=False),
        sa.Column('image_url', sa.String, nullable=False),
        sa.Column('artist_name', sa.String, nullable=False),
        sa.Column('artist_uri', sa.String, nullable=False),
        sa.Column('duration', sa.Integer, nullable=False),  # Milliseconds
    )

    # Create Songs_Playlists join table
    op.create_table(
        'songs_playlists',
        sa.Column('song_id', sa.String, sa.ForeignKey('songs.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
        sa.Column('playlist_id', sa.String, sa.ForeignKey('playlists.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    )

    # Create Categories_Playlists join table
    op.create_table(
        'categories_playlists',
        sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
        sa.Column('playlist_id', sa.String, sa.ForeignKey('playlists.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table('categories_playlists')
    op.drop_table('songs_playlists')
    op.drop_table('songs')
    op.drop_table('playlists')
    op.drop_table('categories')
