# api.py
from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'weather_model.pkl')
model = joblib.load(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        humidity = data['humidity']
        wind_speed = data['windSpeed']

        features = [np.array([humidity, wind_speed])]

        prediction = model.predict(features)

        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)