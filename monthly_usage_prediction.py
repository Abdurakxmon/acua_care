import pandas as pd
import joblib
import tensorflow as tf
import numpy as np
import prophet

# version1

# This model except the last 30 days total daily water usage. Based on that, It will predict for the next 30 days total water usage
# pip install tensorflow==2.17 prophet 

lstm_model = tf.keras.models.load_model("monthly_water_predictor.keras")
month_list = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]


sample_30_day_data = np.array([ 283.37059493,  579.79522908,  650.21023669,  699.3252922 ,
        374.74117434,  705.50961656,  410.2737762 ,  235.38226629,
        439.63099057,  555.68496225,  902.19813995,  257.45984287,
        269.12696168,  353.91089228,  275.52744991,  470.60667915,
        747.39056257,  509.74697703,  351.99132965,  468.37449205,
        445.85571882, 1034.97929641,  461.61554589,  779.59691881,
        528.18620966,  220.75640326,  256.38206611,  755.22944698,
        681.83707061, 1190.25202912])

X_test_sample = sample_30_day_data.reshape((-1,1))

input_sequence = np.array(X_test_sample).reshape(1, 30, 1)

future_predictions = []

for _ in range(30):
    next_day_prediction = lstm_model.predict(input_sequence)
    
    future_predictions.append(next_day_prediction[0][0])
    
    next_day_prediction = np.reshape(next_day_prediction, (1, 1, 1))
    
    input_sequence = np.append(input_sequence[:, 1:, :], next_day_prediction, axis=1)

future_predictions = np.array(future_predictions)
print(np.sum(future_predictions), "Liter will be used in the next 30 days.")


# version2
X_data = {
    'ds': pd.to_datetime(['2024-09-01', '2024-09-02', '2024-09-03', '2024-09-04',
               '2024-09-05', '2024-09-06', '2024-09-07', '2024-09-08',
               '2024-09-09', '2024-09-10', '2024-09-11', '2024-09-12',
               '2024-09-13', '2024-09-14', '2024-09-15', '2024-09-16',
               '2024-09-17', '2024-09-18', '2024-09-19', '2024-09-20',
               '2024-09-21', '2024-09-22', '2024-09-23', '2024-09-24',
               '2024-09-25', '2024-09-26', '2024-09-27', '2024-09-28',
               '2024-09-29', '2024-09-30']), 

    'y': sample_30_day_data
}
train_df = pd.DataFrame(X_data)
current_month = train_df.ds.dt.month.unique()[0]
print(train_df.info())

prophet_model = prophet.Prophet()
prophet_model.fit(train_df)

future = prophet_model.make_future_dataframe(periods=31)

forecast = prophet_model.predict(future)
next_month = current_month + 1 if current_month < 12 else 1
next_month_total_water_usage = forecast[forecast["ds"].dt.month == next_month]["yhat"].sum()
print(next_month_total_water_usage, f"Liter will be used in {month_list[next_month-1]}")