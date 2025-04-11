import datetime
import uuid

from typing import Optional
from sqlalchemy import Uuid, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class ReviewAuthorStats(Base):
    """
    Stores the snapshot of an author's statistics at the time a specific
    review was created/fetched. Linked one-to-one with a Review.
    """
    __tablename__ = "review_author_stats"

    # Foreign Key to the Review this snapshot belongs to (One-to-One)
    review_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("review.id", ondelete="CASCADE"), # Cascade delete if Review is deleted
        unique=True,  # Enforces one-to-one at DB level
        nullable=False,
        index=True
    )

    # Stats from the 'author' block of the review API response
    num_games_owned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    num_reviews: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    playtime_forever: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    playtime_last_two_weeks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    playtime_at_review: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # NOTE: API provides Unix timestamp; convert to datetime before saving.
    last_played: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationship back to the Review (One-to-One)
    review: Mapped["Review"] = relationship(
        "Review",
        back_populates="author_stats"
    )

    def __repr__(self):
        return f"<ReviewAuthorStats(id={self.id}, review_id={self.review_id})>"
