from django.shortcuts import render
# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import RegisterSerializer
import joblib
import pandas as pd
from main.models import Profile
from datetime import date


# {
#     "first_name":"first_name",
#     "last_name":"last_name",
#     "email":"email@ew.wq",
#     "password":"password",
#     "profile":{
#         "phone":"phone",
#         "address":"address"
#     }
# }

water_gradient_model = joblib.load("models/water_forest_model.joblib")
cooking_linear_model = joblib.load("models/cooking_forest_model.joblib")
dish_linear_model = joblib.load("models/dish_forest_model.joblib")
laundry_linear_model = joblib.load("models/laundry_forest_model.joblib")
showers_forest_model = joblib.load("models/showers_linear_model.joblib")
toilet_linear_model = joblib.load("models/toilet_forest_model.joblib")

water_sd = joblib.load("scalers/water_sd_scaler.joblib")
dish_sd = joblib.load("scalers/dish_sd_scaler.joblib")
laundry_sd = joblib.load("scalers/laundry_sd_scaler.joblib")
showers_sd = joblib.load("scalers/showers_sd_scaler.joblib")
toilet_sd = joblib.load("scalers/toilet_sd_scaler.joblib")
cooking_sd = joblib.load("scalers/cooking_sd_scaler.joblib")

models_list = [water_gradient_model, cooking_linear_model, dish_linear_model,
               laundry_linear_model, showers_forest_model, toilet_linear_model]

scalers_list = [water_sd, cooking_sd, dish_sd, laundry_sd, showers_sd, toilet_sd]

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SettingsView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view
    def post(self, request):
        ls = [
            'daily',
            'number_of_people',
            'watering_garden',
            'cooking',
            'dishwashing',
            'laundry',
            'showers',
            'toilet_flush'
        ]
        # {
        #     'daily': 1,
        #     'number_of_people': 1,
        #     'watering_garden': ['7:30', '20:00'],
        #     'cooking': ['12:30', '18:00'],
        #     'dishwashing': ['12:30', '18:00'],
        #     'laundry': ['13:30', '19:00'],
        #     'showers': ['12:30', '18:00'],
        #     'toilet_flush': ['12:30', '18:00'],
        # }
        profile = Profile.objects.get(user=request.user)
        data = request.data
        for i in ls:
            if i not in data:
                return Response({"status": 0,"message": f"{i} field is required!"},status=status.HTTP_400_BAD_REQUEST)

        time_values = [0 for hour in range(24*60)]
        features = ["Watering Garden", "Cooking", "Dishwashing", "Laundry", "Showers", "Toilet Flush"]
        per_values = {}

        for model, scaler, feature, i in zip(models_list, scalers_list, features, ls[2:]):
            try: feature_times = len(data[i])
            except: feature_times = 0
            df = pd.DataFrame({"Family Size": [data["number_of_people"]], feature: feature_times})
            X_sample = df.values
            X_sample_scaled = scaler.transform(X_sample)
            try: per_values[i]=round(model.predict(X_sample_scaled)[0]/feature_times, 2)
            except: per_values[i]=0

        for i in ls[2:]:
            for j in data[i]:
                try:
                    a=j.split(":")
                    cur=int(a[0])*60+int(a[1])
                    time_values[cur]+=per_values[i]
                except: continue
        for i in range(1,1440):
            time_values[i]+=time_values[i-1]

        profile.number_of_people = data["number_of_people"]
        profile.watering_garden = data["watering_garden"]
        profile.cooking = data["cooking"]
        profile.dishwashing = data["dishwashing"]
        profile.laundry = data["laundry"]
        profile.showers = data["showers"]
        profile.toilet_flush = data["toilet_flush"]

        if data["daily"]:
            profile.day = date.today()
            profile.total_daily = time_values
        else:
            profile.day = None
            profile.total = time_values
        profile.save()

        return Response({"status": 1})
    # print( datetime.now().date())

class NextMonthView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def post(self, request):
        data = request.data
        if 'cur_month' not in data:
            return Response({"status": 0, "message": "cur_month field is required!"},
                                status=status.HTTP_400_BAD_REQUEST)
        month_list = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
                      "october", "november", "december"]

        if data["cur_month"] not in month_list:
            return Response({"status": 0, "message": "cur_month field is invalid!"},
                                status=status.HTTP_400_BAD_REQUEST)

        monthly_water_usage_model = joblib.load("mothly_water_usage_model.joblib")

        ds = monthly_water_usage_model.make_future_dataframe(periods=30)

        prediction_df = monthly_water_usage_model.predict(ds)


        year = 2020
        previous_month = data["cur_month"]
        month_index = (month_list.index(previous_month) + 1) % len(month_list)
        next_month_index = month_index + 1

        pred_for_next_month = prediction_df[
            (prediction_df['ds'].dt.year == year) & (prediction_df['ds'].dt.month == next_month_index)
            ]["yhat"]
        next_month_water_usage = pred_for_next_month.sum()



        return Response({"status": 1, "next_month":round(next_month_water_usage,2)})
    # print( datetime.now().date())

