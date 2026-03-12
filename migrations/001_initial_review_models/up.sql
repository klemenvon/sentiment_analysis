CREATE TABLE authors (
    id TEXT PRIMARY KEY,
    steamid TEXT NOT NULL UNIQUE,
    num_games_owned INT NOT NULL,
    num_reviews INT NOT NULL,
    playtime_forever INT NOT NULL,
    playtime_last_two_weeks INT NOT NULL,
    playtime_at_review INT NOT NULL,
    last_playtime_update INT NOT NULL
);

CREATE TABLE games (
    id TEXT PRIMARY KEY,
    appid INT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    last_modified INT NOT NULL,
    price_change_number INT NOT NULL
);

CREATE TABLE reviews (
    id TEXT PRIMARY KEY,
    author_id TEXT NOT NULL REFERENCES authors(id),
    game_id TEXT NOT NULL REFERENCES games(id),
    recommendationid INT NOT NULL,
    language TEXT,
    review TEXT,
    timestamp_created INT NOT NULL,
    timestamp_updated INT NOT NULL,
    voted_up BOOLEAN NOT NULL,
    votes_up INT NOT NULL,
    votes_funny INT NOT NULL,
    weighted_vote_score REAL NOT NULL,
    comment_count INT NOT NULL,
    steam_purchase BOOLEAN NOT NULL,
    received_for_free BOOLEAN NOT NULL,
    written_during_early_access BOOLEAN NOT NULL,
    primarily_steam_deck BOOLEAN NOT NULL
);

CREATE INDEX ix_reviews_author_id ON reviews(author_id);
CREATE INDEX ix_reviews_game_id ON reviews(game_id);
