from uuid import uuid4

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


def new_uuid() -> str:
    return str(uuid4())


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_uuid)
    author_id: Mapped[str] = mapped_column(String, ForeignKey("authors.id"), nullable=False)
    game_id: Mapped[str] = mapped_column(String, ForeignKey("games.id"), nullable=False)
    recommendationid: Mapped[int] = mapped_column(nullable=False)
    language: Mapped[str | None] = mapped_column(nullable=True)
    review: Mapped[str | None] = mapped_column(nullable=True)
    timestamp_created: Mapped[int] = mapped_column(nullable=False)
    timestamp_updated: Mapped[int] = mapped_column(nullable=False)
    voted_up: Mapped[bool] = mapped_column(nullable=False)
    votes_up: Mapped[int] = mapped_column(nullable=False)
    votes_funny: Mapped[int] = mapped_column(nullable=False)
    weighted_vote_score: Mapped[float] = mapped_column(nullable=False)
    comment_count: Mapped[int] = mapped_column(nullable=False)
    steam_purchase: Mapped[bool] = mapped_column(nullable=False)
    received_for_free: Mapped[bool] = mapped_column(nullable=False)
    written_during_early_access: Mapped[bool] = mapped_column(nullable=False)
    primarily_steam_deck: Mapped[bool] = mapped_column(nullable=False)

    author: Mapped["ReviewAuthor"] = relationship("ReviewAuthor", back_populates="reviews")
    game: Mapped["Game"] = relationship("Game", back_populates="reviews")

    __table_args__ = (
        Index("ix_reviews_author_id", "author_id"),
        Index("ix_reviews_game_id", "game_id"),
    )


class ReviewAuthor(Base):
    __tablename__ = "authors"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_uuid)
    steamid: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    num_games_owned: Mapped[int] = mapped_column(nullable=False)
    num_reviews: Mapped[int] = mapped_column(nullable=False)
    playtime_forever: Mapped[int] = mapped_column(nullable=False)
    playtime_last_two_weeks: Mapped[int] = mapped_column(nullable=False)
    playtime_at_review: Mapped[int] = mapped_column(nullable=False)
    last_playtime_update: Mapped[int] = mapped_column(nullable=False)

    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="author")


class Game(Base):
    __tablename__ = "games"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_uuid)
    appid: Mapped[int] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    last_modified: Mapped[int] = mapped_column(nullable=False)
    price_change_number: Mapped[int] = mapped_column(nullable=False)

    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="game")
