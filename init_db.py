import os

from sqlalchemy import create_engine

# --- Import models ---
# Import all of the models, even if we don't call them explicitly, if the ORM doesn't
# know about them, we won't get the tables created.
from models import (
    Base,
    Author,
    Review,
    ReviewAuthorStats,
)

# --- Init Variables ---
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'test_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'postgres')

# --- Construct URL ---
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"Connecting to database: postgresql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")


def create_tables():
    """Creates the database tables which will hold our models."""
    try:
        engine = create_engine(DATABASE_URL, echo=True)

        print("Creating tables...")
        Base.metadata.create_all(engine)
        print("Tables successfully created.")

    except Exception as e:
        print(f"An error occurred during table creation: {e}")

if __name__ == "__main__":
    # If we run this script, tables should be created
    create_tables()
