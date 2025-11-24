# train_rain_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

print("--- Starting Rain Model Training ---")

# --- 1. Load Data ---
try:
    data = pd.read_csv('weather_data.csv')
    print("✅ Data loaded successfully.")
except FileNotFoundError:
    print("❌ ERROR: 'weather_data.csv' not found. Make sure it's in the 'backend' folder.")
    exit()

# --- 2. Data Cleaning and Feature Engineering ---
data = data.dropna(subset=['Precip Type', 'Temperature (C)', 'Apparent Temperature (C)', 'Humidity', 'Pressure (millibars)'])

# Create a binary target variable: 1 for 'rain', 0 for 'snow' or other types
data['Will_Rain'] = (data['Precip Type'] == 'rain').astype(int)
print(f"Data shape after cleaning: {data.shape}")

# --- 3. Check for Class Imbalance (Crucial Info!) ---
rain_counts = data['Will_Rain'].value_counts()
print("\n--- Class Distribution ---")
print(f"Count of 'No Rain' (0): {rain_counts.get(0, 0)}")
print(f"Count of 'Rain' (1):    {rain_counts.get(1, 0)}")
print("--------------------------\n")

# --- 4. Define Features and Target ---
features = ['Temperature (C)', 'Apparent Temperature (C)', 'Humidity', 'Pressure (millibars)']
target = 'Will_Rain'

X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print("✅ Data split into training and testing sets.")

# --- 5. Scale the Features ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("✅ Features scaled successfully.")

# --- 6. Train the Model (with the fix!) ---
# class_weight='balanced' tells the model to give equal importance to both 'rain' and 'no rain'
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_scaled, y_train)
print("✅ Model training complete.")

# Check accuracy on the test set
accuracy = model.score(X_test_scaled, y_test)
print(f"📊 Model accuracy on test data: {accuracy:.4f}")

# --- 7. Save Both Model and Scaler ---
joblib.dump(model, 'rain_model.pkl')
joblib.dump(scaler, 'rain_scaler.pkl')
print("\n🚀 Model and Scaler have been saved successfully!")
print("   -> rain_model.pkl")
print("   -> rain_scaler.pkl")