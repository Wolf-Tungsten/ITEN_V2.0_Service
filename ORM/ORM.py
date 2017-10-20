import config
import datetime as dt
from .Data_Model.DataModel import DataModel
from .Data_Base.DataBase import DataBase


class ORM(object):

    def __init__(self, db):
        self.model = DataModel()
        self.db = DataBase(db)






