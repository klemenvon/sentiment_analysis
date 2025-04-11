from typing import List
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Author(Base):
    """
    Data storage class for a Steam user profile. Contains the persistent ID.
    """
    __tablename__ = "author"

    # steamid is the unique business key from Steam
    steamid: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, nullable=False)

    # Relationship to the reviews written by this author
    # An Author can have many Reviews
    reviews: Mapped[List["Review"]] = relationship(
        "Review",
        back_populates="author",
        # cascade="all, delete-orphan" # Decide if deleting an author should delete their reviews
    )

    def __repr__(self):
        return f"<Author(id={self.id}, steamid={self.steamid})>"
