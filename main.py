import numpy as np
import pandas as pd
import joblib
import detector
import response
import os

DATA_FOLDER = "data"

# Load dataset structure to match features
def preprocess_test_data():
    """Load multiple test datasets and ensure feature consistency with training."""
    try:
        # Load trained model feature names
        sample_df = pd.read_csv(os.path.join(DATA_FOLDER, "filename.csv"))  
        feature_names = sample_df.select_dtypes(include=[np.number]).columns.tolist()

        all_data = []

        # Iterate over all CSV files in the data folder
        for file in os.listdir(DATA_FOLDER):
            if file.endswith(".csv"):
                file_path = os.path.join(DATA_FOLDER, file)
                df = pd.read_csv(file_path)

                # Ensure test data matches trained model structure
                df = df[feature_names]  # Keep only numerical columns
                df.fillna(0, inplace=True)  # Handle missing values
                all_data.append(df.to_numpy())

        return np.vstack(all_data) if all_data else None

    except Exception as e:
        print(f"[ERROR] Data preprocessing failed: {e}")
        return None

# Load trained model
detector_model = joblib.load(os.path.join(DATA_FOLDER, "model.pkl"))

# Preprocess the test data
test_data = preprocess_test_data()

if test_data is not None:
    # Predict anomalies
    predictions = detector_model.predict(test_data)

    # Take action if anomalies are detected
    for i, pred in enumerate(predictions):
        if pred == -1:
            malicious_ip = f"192.168.1.{100 + i}"  # Simulated attacker's IP
            response.block_ip(malicious_ip)
            response.log_threat(malicious_ip)
            print(f"[SYSTEM] Threat detected in row {i}, IP: {malicious_ip} - Action taken.")
        else:
            print(f"[SYSTEM] Row {i}: No threats detected.")
else:
    print("[ERROR] Could not process test data. Ensure the dataset is formatted correctly.")
