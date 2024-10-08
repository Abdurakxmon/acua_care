import sklearn 
import joblib
import pandas as pd

# pip install pandas scikit-learn joblib 

#models should be load outside of the function and classes
water_gradient_model = joblib.load("water_gradient_model.joblib")
cooking_linear_model = joblib.load("cooking_linear_model.joblib")
dish_linear_model = joblib.load("dish_linear_model.joblib")
laundry_linear_model = joblib.load("laundry_gradient_model.joblib")
showers_forest_model = joblib.load("showers_forest_model.joblib")
toilet_linear_model = joblib.load("toilet_linear_model.joblib")
sd_scaler = joblib.load("sd_scaler.joblib")

models_list = [water_gradient_model, cooking_linear_model, dish_linear_model, 
                laundry_linear_model, showers_forest_model, toilet_linear_model]

# you can replace these sample values from ones which came from post request.
sample_data = {"Family Size": [6], "Total Water Usage (Liters)": [1190]}

df = pd.DataFrame(sample_data)

X_sample = df.values

X_sample_scaled = sd_scaler.transform(X_sample)

for model in models_list:
    print(model.predict(X_sample_scaled)[0], "Liter")


# water prediction

# model should be loaded outside classes and funtions
water_quality_classifier = joblib.load("rf_model_water_quality_classifier.jbl")

classes = ["Not Potable", "Potable"]

# actual_result = "Not portable"

# you can replace these sample values from ones which came from post request.
sample_data2 = {"ph": [8.316766], "Hardness": [214.373394], "Solids": [22018.417441], 
"Chloramines": [8.059332], "Sulfate": [356.886136], "Conductivity": [363.266516],
 "Organic_carbon": [18.436524], "Trihalomethanes": [100.341674], "Turbidity": [4.628771	]}


df2 = pd.DataFrame(sample_data2)
df2["pH_difference"] = abs(df2['ph'].values[0] - 7.0)
df2['ratio_tds_to_hardness'] = df2['Solids'] / df2['Hardness']
X_sample2 = df2

water_prediction = water_quality_classifier.predict(X_sample2)[0]
print("Water is:", classes[water_prediction])