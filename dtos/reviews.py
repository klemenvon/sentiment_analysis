# Pydantic validators for the reviews coming from the Steam API.
from pydantic import BaseModel


class AuthorData(BaseModel):
    steamid: str
    num_games_owned: int
    num_reviews: int
    playtime_forever: int
    playtime_last_two_weeks: int
    playtime_at_review: int
    last_played: int


class ReviewData(BaseModel):
    recommendationid: int
    author: AuthorData
    language: str | None = None
    review: str | None = None
    timestamp_created: int
    timestamp_updated: int
    voted_up: bool
    votes_up: int
    votes_funny: int
    weighted_vote_score: float
    comment_count: int
    steam_purchase: bool
    received_for_free: bool
    written_during_early_access: bool
    primarily_steam_deck: bool
    game_appid: int  # Added to identify the game


class GameData(BaseModel):
    appid: int
    name: str
    last_modified: int
    price_change_number: int
