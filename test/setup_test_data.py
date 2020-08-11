import bcrypt

from sqlalchemy     import text
from datetime       import datetime, timedelta


def setup_test_data(database):
    hashed_password = bcrypt.hashpw(
        b'test_password',
        bcrypt.gensalt()
    )