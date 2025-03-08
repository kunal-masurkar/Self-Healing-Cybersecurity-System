import numpy as np
import pandas as pd
import joblib
import detector
import response
import os

DATA_FOLDER = "data"
MODEL_PATH = os.path.join(DATA_FOLDER, "model.pkl")

# Check if model exists
if not os.path.exists(MODEL_PATH):
    print(f"[ERROR] Model file '{MODEL_PATH}' not found. Train the model first.")
    exit()

# Load dataset structure to match features
def preprocess_test_data():
    """Load multiple test datasets and ensure feature consistency with training."""
    try:
        # Load trained model feature names
        sample_path = os.path.join(DATA_FOLDER, "sample1.csv")
        if not os.path.exists(sample_path):
            print(f"[ERROR] Sample dataset '{sample_path}' not found. Ensure a correct sample exists.")
            return None

        sample_df = pd.read_csv(sample_path)
        feature_names = sample_df.select_dtypes(include=[np.number]).columns.tolist()

        all_data = []
        for file in os.listdir(DATA_FOLDER):
            if file.endswith(".csv") and file != "sample1.csv":  # Ignore sample file
                file_path = os.path.join(DATA_FOLDER, file)
                df = pd.read_csv(file_path)

                # Ensure test data matches trained model structure
                df = df.reindex(columns=feature_names, fill_value=0)  # Handle missing columns
                df.fillna(0, inplace=True)  # Handle missing values
                all_data.append(df.to_numpy())

        return np.vstack(all_data) if all_data else None

    except Exception as e:
        print(f"[ERROR] Data preprocessing failed: {e}")
        return None

# Load trained model
detector_model = joblib.load(MODEL_PATH)

# Preprocess the test data
test_data = preprocess_test_data()

if test_data is not None:
    # Predict anomalies
    predictions = detector_model.predict(test_data)

    # Take action if anomalies are detected
    for i, pred in enumerate(predictions):
        if pred == -1:
            malicious_ip = f"192.168.1.{100 + i}"  # Simulated attacker's IP
            try:
                response.block_ip(malicious_ip)
                response.log_threat(malicious_ip)
                print(f"[SYSTEM] Threat detected in row {i}, IP: {malicious_ip} - Action taken.")
            except Exception as e:
                print(f"[ERROR] Failed to block IP {malicious_ip}: {e}")
        else:
            print(f"[SYSTEM] Row {i}: No threats detected.")
else:
    print("[ERROR] Could not process test data. Ensure the dataset is formatted correctly.")
