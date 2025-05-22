import joblib
import pandas as pd

# Load the saved model and metadata
model = joblib.load('models/accident_prediction_model.pkl')
feature_names = joblib.load('models/feature_names.pkl')
label_encoders = joblib.load('models/label_encoders.pkl')

def get_user_input():
    inputs = {}
    print("Welcome to the Accident Prediction Chatbot!")
    print("Please provide the following information:\n")
    
    for feature in feature_names:
        if feature in label_encoders:
            # Handle categorical features
            print(f"Available options for {feature}:")
            options = label_encoders[feature].classes_
            for idx, option in enumerate(options):
                print(f"{idx}: {option}")
            value = int(input(f"{feature} (enter the corresponding number): "))
            inputs[feature] = value
        else:
            # Handle numerical features
            value = int(input(f"{feature}: "))
            inputs[feature] = value
    return inputs

def accident_prediction_chatbot():
    user_inputs = get_user_input()
    
    # Create DataFrame with all required features
    user_data = pd.DataFrame([user_inputs])
    
    # Ensure feature order matches the model's expectations
    user_data = user_data[feature_names]
    
    # Make prediction
    prediction = model.predict(user_data)
    predicted_label = label_encoders['crash_type'].inverse_transform(prediction)
    print(f"\nPrediction: The predicted crash type is {predicted_label[0]}.")

if __name__ == "__main__":
    accident_prediction_chatbot()