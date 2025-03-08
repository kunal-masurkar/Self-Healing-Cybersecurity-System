import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)

    def load_data(self):
        try:
            # Load multiple CSV files in 'data/' folder (if any)
            import os
            dataframes = []
            for file in os.listdir("data"):
                if file.endswith(".csv"):
                    df = pd.read_csv(f"data/{file}")
                    dataframes.append(df)

            # Merge all datasets
            data = pd.concat(dataframes, ignore_index=True)
            
            # Drop non-numeric columns (like IP addresses)
            data = data.select_dtypes(include=[np.number])
            
            # Handle missing values
            data = data.fillna(0)

            return data

        except Exception as e:
            print(f"[ERROR] Failed to load data: {e}")
            return None

    def train(self):
        """ Train the Isolation Forest model with processed data. """
        data = self.load_data()
        if data is None or data.empty:
            print("[ERROR] No valid training data found.")
            return
        
        self.model.fit(data)
        joblib.dump(self.model, "data/model.pkl")
        print("[INFO] Model trained and saved as 'model.pkl'.")

    def predict(self, new_data):
        """ Load the model and predict anomalies in new data. """
        self.model = joblib.load("data/model.pkl")
        return self.model.predict(new_data)

# Run training
if __name__ == "__main__":
    detector = AnomalyDetector()
    detector.train()
