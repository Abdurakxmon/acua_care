import prophet
import pandas as pd
import joblib

# pip install prophet 

monthly_water_usage_model = joblib.load("mothly_water_usage_model.joblib")

ds = monthly_water_usage_model.make_future_dataframe(periods=30)

prediction_df = monthly_water_usage_model.predict(ds)

months = list(range(1, 13))

month_list = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
year = 2020
previous_month = "september"
month_index = month_list.index(previous_month) + 1
next_month_index = month_index + 1

pred_for_october = prediction_df[(prediction_df['ds'].dt.year == year) & (prediction_df['ds'].dt.month == next_month_index)]["yhat"]
next_month_water_usage = pred_for_october.sum()
print(next_month_water_usage, "Liters")

# print(prediction_df.head(30)[["ds", "yhat"]])

