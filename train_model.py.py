import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

def train_accident_model(data_path):
    # Load the data
    df = pd.read_csv(data_path)
    
    # Handle missing values
    for col in df.select_dtypes(include='object').columns:
        df[col].fillna(df[col].mode()[0], inplace=True)
    for col in df.select_dtypes(include='number').columns:
        df[col].fillna(df[col].median(), inplace=True)
    
    # Encode categorical variables
    label_encoders = {}
    for col in df.select_dtypes(include='object').columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
        
    # Define features and target
    X = df.drop(['crash_type', 'crash_date'], axis=1)  # Removing date and target variables
    y = df['crash_type']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model and feature names
    joblib.dump(model, 'models/accident_prediction_model.pkl')
    joblib.dump(list(X.columns), 'models/feature_names.pkl')
    joblib.dump(label_encoders, 'models/label_encoders.pkl')
    
    return model, label_encoders, list(X.columns)

if __name__ == "__main__":
    train_accident_model('data/traffic_accidents.csv')