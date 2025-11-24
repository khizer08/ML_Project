# api.py
from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# --- Load All Models and Scalers on Startup ---
try:
    # Get the absolute path to the directory this script is in
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load Temperature Model
    temp_model_path = os.path.join(script_dir, 'weather_model.pkl')
    temp_model = joblib.load(temp_model_path)

    # Load Rain Model
    rain_model_path = os.path.join(script_dir, 'rain_model.pkl')
    rain_model = joblib.load(rain_model_path)
    
    # Load Rain Scaler
    rain_scaler_path = os.path.join(script_dir, 'rain_scaler.pkl')
    rain_scaler = joblib.load(rain_scaler_path)
    
    print("✅ All models and scalers loaded successfully.")

except FileNotFoundError as e:
    print(f"❌ ERROR: A required model or scaler file is missing.")
    print(f"   -> {e.filename}")
    print("   -> Please run the training scripts first!")
    exit()

@app.route('/predict-temp', methods=['POST'])
def predict_temp():
    try:
        data = request.get_json()
        humidity = data['humidity']
        wind_speed = data['windSpeed']
        
        # Create a 2D numpy array for a single prediction
        features = np.array([[humidity, wind_speed]])
        
        prediction = temp_model.predict(features)
        
        # prediction[0] gets the single value from the numpy array
        return jsonify({'prediction': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict-rain', methods=['POST'])
def predict_rain():
    try:
        data = request.get_json()
        
        # Step 1: Create a 2D numpy array with the raw input features
        raw_features = np.array([[
            data['temperature'],
            data['apparentTemperature'],
            data['humidity'],
            data['pressure']
        ]])
        
        # Step 2: Use the loaded scaler to transform the raw features
        scaled_features = rain_scaler.transform(raw_features)
        
        # Step 3: Predict using the SCALED features
        prediction = rain_model.predict(scaled_features)
        
        print(f"RAW MODEL OUTPUT: {prediction}") # This will be [0] or [1]
        
        # Step 4: Convert the prediction (0 or 1) to a user-friendly string
        result = 'Yes, it will likely rain.' if prediction[0] == 1 else 'No, it likely won\'t rain.'
        
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask API server...")
    app.run(host='0.0.0.0', port=5000)