from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)
script_dir = os.path.dirname(os.path.abspath(__file__))

temp_model_path = os.path.join(script_dir, 'weather_model.pkl')
temp_model = joblib.load(temp_model_path)

rain_model_path = os.path.join(script_dir, 'rain_model.pkl')
rain_model = joblib.load(rain_model_path)

@app.route('/predict-temp', methods=['POST'])
def predict_temp():
    try:
        data = request.get_json()
        humidity = data['humidity']
        wind_speed = data['windSpeed']
        features = [np.array([humidity, wind_speed])]
        prediction = temp_model.predict(features)
        return jsonify({'prediction': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict-rain', methods=['POST'])
def predict_rain():
    try:
        data = request.get_json()
        features = [np.array([
            data['temperature'],
            data['apparentTemperature'],
            data['humidity'],
            data['pressure']
        ])]
        prediction = rain_model.predict(features)
        result = 'Yes, it will likely rain.' if prediction[0] == 1 else 'No, it likely won\'t rain.'
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)