import json
import joblib
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
import asyncio
from rest_framework_simplejwt.exceptions import TokenError
import os



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

        user = await self.get_user(token['user_id'])

        if user and user.is_authenticated:
            self.scope['user'] = user
            await self.run_periodic_task()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def run_periodic_task(self):
        while True:
            monthly_water_usage_model = joblib.load("mothly_water_usage_model.joblib")

            ds = monthly_water_usage_model.make_future_dataframe(periods=30)

            prediction_df = monthly_water_usage_model.predict(ds)

            month_list = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
                          "october", "november", "december"]
            year = 2020
            previous_month = "december"
            month_index = (month_list.index(previous_month) + 1) % len(month_list)
            next_month_index = month_index + 1

            pred_for_next_month = prediction_df[
                (prediction_df['ds'].dt.year == year) & (prediction_df['ds'].dt.month == next_month_index)
            ]["yhat"]
            next_month_water_usage = pred_for_next_month.sum()

            await self.send(text_data=json.dumps({
                'next_month': next_month_water_usage
            }))

            await asyncio.sleep(3600)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
