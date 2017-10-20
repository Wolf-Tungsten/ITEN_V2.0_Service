from .collections.user import UserCollection
from .collections.machine_arguments import MachineArguments
from .collections.train_mode import TrainMode
from .collections.video_playback import VideoPlayback


class DataBase(object):
    def __init__(self, db):
        self.db = db

        self.user = UserCollection(self.db)
        self.machine_arguments = MachineArguments(self.db)
        self.train_mode = TrainMode(self.db)
        self.video_playback = VideoPlayback(self.db)

