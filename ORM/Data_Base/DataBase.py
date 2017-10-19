from .collections.user import UserCollection
from .collections.machine_arguments import MachineArguments


class DataBase(object):
    def __init__(self, db):
        self.db = db

        self.user = UserCollection(self.db)
        self.machine_arguments = MachineArguments(self.db)

