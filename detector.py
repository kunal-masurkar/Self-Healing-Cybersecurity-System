import numpy as np
import pandas as pd
import os
import joblib
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)

    def load_data(self, data_folder="data"):
        all_data = []
        for file in os.listdir(data_folder):
            if file.endswith(".csv"):
                file_path = os.path.join(data_folder, file)
                df = pd.read_csv(file_path)
                all_data.append(df.values)  # Convert to NumPy array
        if all_data:
            return np.vstack(all_data)  # Combine all datasets
        else:
            raise ValueError("No valid CSV data files found in the 'data' folder.")

    def train(self):
        data = self.load_data()
        self.model.fit(data)
        joblib.dump(self.model, "model.pkl")
        print("[INFO] Model trained and saved.")

    def predict(self, data):
        self.model = joblib.load("model.pkl")
        return self.model.predict(data)

# Example training
if __name__ == "__main__":
    detector = AnomalyDetector()
    detector.train()
