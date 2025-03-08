import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import RobustScaler

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.scaler = RobustScaler()

    def load_data(self):
        """ Load and preprocess data from the 'data/' folder. """
        try:
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                print(f"[INFO] Please place your CSV files in '{data_dir}' and run again.")
                return None
            
            csv_files = [file for file in os.listdir(data_dir) if file.endswith(".csv")]
            if not csv_files:
                print(f"[ERROR] No CSV files found in '{data_dir}'.")
                return None
            
            dataframes = [pd.read_csv(os.path.join(data_dir, file)) for file in csv_files]
            data = pd.concat(dataframes, ignore_index=True).select_dtypes(include=[np.number])
            
            data = data.replace([np.inf, -np.inf], np.nan).fillna(0)
            data = pd.DataFrame(self.scaler.fit_transform(data), columns=data.columns)
            
            print(f"[INFO] Loaded {len(data)} records with {len(data.columns)} features.")
            return data
        except Exception as e:
            print(f"[ERROR] Failed to load data: {e}")
            return None

    def train(self):
        """ Train the Isolation Forest model. """
        data = self.load_data()
        if data is None or data.empty:
            print("[ERROR] No valid training data found.")
            return
        
        try:
            print("[INFO] Training Isolation Forest model...")
            self.model.fit(data)
            os.makedirs("data", exist_ok=True)
            joblib.dump(self.model, "data/model.pkl")
            joblib.dump(self.scaler, "data/scaler.pkl")
            print("[INFO] Model and scaler saved to 'data/' folder.")
        except Exception as e:
            print(f"[ERROR] Failed to train model: {e}")

    def predict(self, new_data):
        """ Predict anomalies in new data. """
        try:
            self.model = joblib.load("data/model.pkl")
            self.scaler = joblib.load("data/scaler.pkl")
            
            if isinstance(new_data, pd.DataFrame):
                new_data = new_data.select_dtypes(include=[np.number]).replace([np.inf, -np.inf], np.nan).fillna(0)
                new_data = pd.DataFrame(self.scaler.transform(new_data), columns=new_data.columns)
            
            return self.model.predict(new_data)
        except Exception as e:
            print(f"[ERROR] Prediction failed: {e}")
            return None

    def predict_file(self, file_path):
        """ Predict anomalies from a CSV file. """
        try:
            new_data = pd.read_csv(file_path)
            original_data = new_data.copy()
            numeric_data = new_data.select_dtypes(include=[np.number]).replace([np.inf, -np.inf], np.nan).fillna(0)
            predictions = self.predict(numeric_data)
            
            result = original_data.copy()
            result['anomaly_score'] = self.model.decision_function(self.scaler.transform(numeric_data))
            result['anomaly'] = predictions
            result['is_anomaly'] = result['anomaly'].apply(lambda x: "Yes" if x == -1 else "No")
            
            output_file = file_path.replace('.csv', '_results.csv')
            result.to_csv(output_file, index=False)
            print(f"[INFO] Predictions saved to {output_file}")
            
            return result
        except Exception as e:
            print(f"[ERROR] File prediction failed: {e}")
            return None

if __name__ == "__main__":
    detector = AnomalyDetector()
    detector.train()
    test_file = "data/test.csv"
    if os.path.exists(test_file):
        detector.predict_file(test_file)
