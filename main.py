import numpy as np
import pandas as pd
import os
import detector
import response

def load_test_data(data_folder="data"):
    test_data = []
    for file in os.listdir(data_folder):
        if file.endswith(".csv"):
            file_path = os.path.join(data_folder, file)
            df = pd.read_csv(file_path)
            test_data.append(df.values)
    if test_data:
        return np.vstack(test_data)
    else:
        raise ValueError("No valid CSV files found for testing.")

# Load test data
test_samples = load_test_data()

# Detect anomalies
detector_model = detector.AnomalyDetector()
for sample in test_samples:
    prediction = detector_model.predict(sample.reshape(1, -1))

    if prediction[0] == -1:
        malicious_ip = "192.168.1.100"  # Placeholder IP
        response.block_ip(malicious_ip)
        response.log_threat(malicious_ip)
        print("[SYSTEM] Threat detected & mitigated.")
    else:
        print("[SYSTEM] No threats detected.")