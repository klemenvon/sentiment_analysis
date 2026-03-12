from db.reviews.models import Game, Review, ReviewAuthor
from dtos.reviews import GameData, ReviewData


def add_game(session, game_data: GameData) -> Game:
    # Check if game already exists
    existing_game = session.query(Game).filter_by(appid=game_data.appid).first()
    if existing_game:
        return existing_game

    game = Game(
        appid=game_data.appid,
        name=game_data.name,
        last_modified=game_data.last_modified,
        price_change_number=game_data.price_change_number,
    )
    session.add(game)
    session.flush()  # To get the id
    return game


def bulk_add_games(session, games_data: list[GameData]):
    for game_data in games_data:
        add_game(session, game_data)


def add_review(session, review_data: ReviewData):
    # Handle author
    author_data = review_data.author
    author = session.query(ReviewAuthor).filter_by(steamid=author_data.steamid).first()
    if not author:
        author = ReviewAuthor(
            steamid=author_data.steamid,
            num_games_owned=author_data.num_games_owned,
            num_reviews=author_data.num_reviews,
            playtime_forever=author_data.playtime_forever,
            playtime_last_two_weeks=author_data.playtime_last_two_weeks,
            playtime_at_review=author_data.playtime_at_review,
            last_playtime_update=author_data.last_played,
        )
        session.add(author)
        session.flush()

    # Ensure game exists
    game = session.query(Game).filter_by(appid=review_data.game_appid).first()
    if not game:
        raise ValueError(f"Game with appid {review_data.game_appid} does not exist. Please add the game first.")

    # Create review
    review = Review(
        author_id=author.id,
        game_id=game.id,
        recommendationid=review_data.recommendationid,
        language=review_data.language,
        review=review_data.review,
        timestamp_created=review_data.timestamp_created,
        timestamp_updated=review_data.timestamp_updated,
        voted_up=review_data.voted_up,
        votes_up=review_data.votes_up,
        votes_funny=review_data.votes_funny,
        weighted_vote_score=review_data.weighted_vote_score,
        comment_count=review_data.comment_count,
        steam_purchase=review_data.steam_purchase,
        received_for_free=review_data.received_for_free,
        written_during_early_access=review_data.written_during_early_access,
        primarily_steam_deck=review_data.primarily_steam_deck,
    )
    session.add(review)


def bulk_add_reviews(session, reviews_data: list[ReviewData]):
    for review_data in reviews_data:
        add_review(session, review_data)
