import json

from utils import Requester

class Scraper:
    def __init__(self, db_connection, requester):
        """
        Scraping class which connects to a database through SQLAlchemy and scrapes the Steam API for reviews.
        db_connection: the SQLAlchemy object which allows us to interact with the datbase
        requester (Requester): The requester object we use to get the data from the API
        """
        self.connection = db_connection
        self.requester = requester

    def scrape_game(self, game_id):
        """
        Initializes scraping of all the user reviews on a game with `game_id`
        game_id (uint): the steam ID of the game to scrape
        """
        pass

