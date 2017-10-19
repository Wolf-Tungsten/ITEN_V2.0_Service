from config import (VIDEO_PRESERVE)
from ..collections.base import CollectionBase
import datetime as dt


class VideoPlayback(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'video_playback')

    async def add_video(self, user_id, video_url):
        timestamp = dt.datetime.now().timestamp()
        # 检索超过保留条数设置的视频并删除
        condition = {'user_id': user_id}
        sort = {'timestamp': self.DESCENDING}
        cursor = self.collection.find(condition, sort)
        counter = 0
        async for video_playback in cursor:
            counter = counter + 1
            if counter >= VIDEO_PRESERVE:
                self.delete_one_by_id(str(video_playback['_id']))
        video_playback = {
            'user_id': user_id,
            'timestamp': timestamp,
            'video_url': video_url
        }
        await self.insert_one(video_playback)

    async def get_videos(self, user_id):
        condition = {'user_id': user_id}
        cursor = self.collection.find(condition)
        video_list = []
        async for video_playback in cursor:
            video_list.append(video_playback['video_url'])
        return video_list
