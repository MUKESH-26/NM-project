from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load the model and required files
try:
    model = joblib.load('models/accident_prediction_model.pkl')
    feature_names = joblib.load('models/feature_names.pkl')
    label_encoders = joblib.load('models/label_encoders.pkl')
except:
    print("Warning: Model files not found. Please ensure model is trained first.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Create DataFrame with the input data
        input_data = pd.DataFrame({
            'weather_condition': [data['weather']],
            'lighting_condition': [data['lighting']],
            'roadway_surface_cond': [data['road_surface']],
            'crash_hour': [int(data['hour'])],
            'traffic_control_device': [data['traffic_control']],
            'first_crash_type': [data['crash_type']],
            'alignment': [data['alignment']],
            'prim_contributory_cause': [data['cause']],
            'most_severe_injury': [data['injury']],
            'crash_day_of_week': [4],
            'crash_month': [1],
            'damage': [0],
            'num_units': [1],
            'intersection_related_i': [0],
            'injuries_total': [0],
            'injuries_fatal': [0],
            'injuries_incapacitating': [0],
            'injuries_non_incapacitating': [0],
            'injuries_reported_not_evident': [0],
            'injuries_no_indication': [0],
            'road_defect': [0],
            'trafficway_type': [0]
        })
        
        # Ensure correct feature order
        input_data = input_data[feature_names]
        
        # Make prediction
        prediction = model.predict(input_data)
        prob = model.predict_proba(input_data)
        
        return jsonify({
            'prediction': int(prediction[0]),
            'probability': float(max(prob[0]))
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)