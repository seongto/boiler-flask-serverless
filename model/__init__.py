from .users_dao             import UsersDao
from .samples_dao           import SamplesDao

class Models :
    def __init__(self, database):
        self.users_dao = UsersDao(database)
        self.samples_dao = SamplesDao(database)

    