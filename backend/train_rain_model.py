# train_rain_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

data = pd.read_csv('weather_data.csv')
data = data.dropna() 


data['Will_Rain'] = (data['Precip Type'] == 'rain').astype(int)


features = ['Temperature (C)', 'Apparent Temperature (C)', 'Humidity', 'Pressure (millibars)']
target = 'Will_Rain'

X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

joblib.dump(model, 'rain_model.pkl')

print("✅ Rain prediction model has been trained and saved as rain_model.pkl")