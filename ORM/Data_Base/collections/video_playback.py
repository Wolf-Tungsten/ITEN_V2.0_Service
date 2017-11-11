from config import (VIDEO_PRESERVE, QINIU_DOMAIN)
from ..collections.base import CollectionBase
import datetime as dt
from sdk.qiniu_sdk import delete_video


class VideoPlayback(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'video_playback')

    async def add_video(self, user_id, video_url, key):
        timestamp = dt.datetime.now().timestamp()
        # 检索超过保留条数设置的视频并删除
        condition = {'user_id': user_id}
        sort = [('timestamp',self.DESCENDING)]
        cursor = self.collection.find(condition, sort=sort)
        counter = 0
        async for video_playback in cursor:
            counter = counter + 1
            if counter >= VIDEO_PRESERVE:
                delete_video(video_playback['video_key'])
                await self.delete_one_by_id(str(video_playback['_id']))
        video_playback = {
            'user_id': user_id,
            'timestamp': timestamp,
            'video_url': QINIU_DOMAIN + key,
            'video_key': key
        }
        await self.insert_one(video_playback)

    async def get_videos(self, user_id):
        condition = {'user_id': user_id}
        cursor = self.collection.find(condition)
        video_list = []
        async for video_playback in cursor:
            video_list.append(video_playback['video_url'])
        return video_list
