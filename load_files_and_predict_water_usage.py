import sklearn 
import joblib
import pandas as pd

# pip install pandas scikit-learn joblib 

#models
water_gradient_model = joblib.load("water_gradient_model.joblib")
cooking_linear_model = joblib.load("cooking_linear_model.joblib")
dish_linear_model = joblib.load("dish_linear_model.joblib")
laundry_linear_model = joblib.load("laundry_gradient_model.joblib")
showers_forest_model = joblib.load("showers_forest_model.joblib")
toilet_linear_model = joblib.load("toilet_linear_model.joblib")
sd_scaler = joblib.load("sd_scaler.joblib")

models_list = [water_gradient_model, cooking_linear_model, dish_linear_model, laundry_linear_model, showers_forest_model, toilet_linear_model]

sample_data = {"Family Size": [6], "Total Water Usage (Liters)": [1190]}

df = pd.DataFrame(sample_data)

X_sample = df.values

X_sample_scaled = sd_scaler.transform(X_sample)

for model in models_list:
    print(model.predict(X_sample_scaled)[0], "Liter")