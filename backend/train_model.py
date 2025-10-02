import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

data = pd.read_csv('weather_data.csv')

data = data.dropna()

if 'Loud Cover' in data.columns:
    data = data.drop(columns=['Loud Cover'])

features = ['Humidity', 'Wind Speed (km/h)']
target = 'Temperature (C)'

X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

joblib.dump(model, 'weather_model.pkl')

print("✅ Model has been trained and saved as weather_model.pkl")