import os
from dotenv import load_dotenv

load_dotenv()

class db_config:
    """Configuration holder for DB connection.

    Reads the SQLAlchemy URI from the environment for security. The
    variable to set is `DATABASE_URL` (preferred) or `SQLALCHEMY_DATABASE_URI`.
    If neither is set, falls back to the previous hardcoded Railway URI.
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')