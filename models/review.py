import datetime
from typing import Optional
import uuid
from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    Text,
    ForeignKey,
    Uuid,
    Integer,
    Boolean,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Review(Base):
    """
    Data class containing a specific Steam review, linked to an author and game,
    and associated with a snapshot of the author's stats at that time.
    """
    __tablename__ = "review"

    # --- Core Review Identifiers ---
    recommendationid: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, nullable=False)
    steam_appid: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)

    # --- Link to the Author (Many-to-One) ---
    author_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("author.id"), # Decide ondelete behavior if author deleted
        index=True,
        nullable=False,
    )
    author: Mapped["Author"] = relationship(
        "Author",
        back_populates="reviews"
    )

    # --- Link to the Author Stats Snapshot (One-to-One) ---
    # This relationship links to the ReviewAuthorStats specific to this review
    author_stats: Mapped["ReviewAuthorStats"] = relationship(
        "ReviewAuthorStats",
        back_populates="review",
        cascade="all, delete-orphan", # If review deleted, delete its stats snapshot
        uselist=False # Crucial for One-to-One from this side
    )

    # --- Review Content and Metadata ---
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    review: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # NOTE: API provides Unix timestamps; convert to datetime before saving.
    timestamp_created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    timestamp_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # --- Votes and Scores ---
    voted_up: Mapped[bool] = mapped_column(Boolean, nullable=False)
    votes_up: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    votes_funny: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # NOTE: API provides string; convert to float before saving.
    weighted_vote_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    comment_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # --- Boolean Flags ---
    steam_purchase: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    received_for_free: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    written_during_early_access: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    primarily_steam_deck: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


    def __repr__(self):
        return f"<Review(id={self.id}, recommendationid={self.recommendationid}, author_id={self.author_id})>"
