import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
import asyncio
from rest_framework_simplejwt.exceptions import TokenError
from .models import Profile
from datetime import datetime
from datetime import date


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        token = None

        try:
            token = self.scope['query_string'].decode('utf-8').split('=')[1]
        except Exception as e:
            await self.close()
            return

        await self.accept()

        try:
            token = AccessToken(token)
        except TokenError as e:
            # Handle token expiration or invalid token
            await self.send(text_data=json.dumps({
                'error': 'Invalid or expired token',
                'details': str(e)
            }))
            await self.close()
            return

        user = await self.get_profile(token['user_id'])

        if user:
            self.user= user
            await self.run_periodic_task()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))

    async def run_periodic_task(self):
        while True:
            now = datetime.now()
            cur = now.hour*60+now.minute
            ans=json.loads(self.user.total)[cur]
            if self.user.day==date.today(): ans=json.loads(self.user.total_daily)[cur]
            await self.send(text_data=json.dumps({
                'cur_spending': round(ans,2)
            }))

            await asyncio.sleep(1800)



    @database_sync_to_async
    def get_profile(self, user_id):
        try:
            return Profile.objects.get(user__id=user_id)
        except Profile.DoesNotExist:
            return None
