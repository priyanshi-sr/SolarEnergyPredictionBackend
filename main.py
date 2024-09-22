import joblib
import pandas as pd

# Load the model
model = joblib.load('model.joblib')  # random forest Regressor

# Load the data
features = ['Temperature', 'Pressure', 'Humidity', 'WindDirection(Degrees)', 'Speed']
value = [59.0, 30.43, 85.0, 181.99, 4.5]  # giving input values for prediction to the model (openweather api)

data = dict(zip(features, value))
print(data)

df = pd.DataFrame(data, index=[0])

# Predict
prediction = model.predict(df)[0]  # predicting the output
print(prediction)
