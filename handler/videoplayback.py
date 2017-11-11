from handler.base import BaseHandler
import routes
from handler.exception import PermissionDeniedError, AuthError, ResourceNotExistError
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
import urllib.parse
import json
from tornado.web import RequestHandler


class VideoHandler(BaseHandler):
    async def get(self, operator):
        user_id = await self.user_id
        video_list = await self.db.video_playback.get_videos(user_id)
        self.write({
            'video_list': video_list
        })

    async def post(self, operator):
        user_id = self.get_argument('user_id')
        video_url = self.get_argument('video_url')
        key = self.get_argument('key')
        await self.db.video_playback.add_video(user_id=user_id, video_url=video_url, key=key)
        self.write({
            'flag': True
        })


routes.handlers += [
    (r'/video/([a-z]+)', VideoHandler),
]