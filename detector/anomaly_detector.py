import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from config import MODEL_CONFIG, DATA_DIR, MODEL_PATH, SCALER_PATH
from utils.logger import logger
import os

class EnhancedAnomalyDetector:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.pipeline = Pipeline([
            ('scaler', RobustScaler()),
            ('model', IsolationForest(**MODEL_CONFIG))
        ])

    def _validate_data(self, data):
        """Validate input data format and content."""
        if not isinstance(data, (pd.DataFrame, np.ndarray)):
            raise ValueError("Input data must be a pandas DataFrame or numpy array")
        
        if isinstance(data, pd.DataFrame):
            # Check for non-numeric columns
            non_numeric = data.select_dtypes(exclude=[np.number]).columns
            if not non_numeric.empty:
                logger.warning(f"Dropping non-numeric columns: {non_numeric.tolist()}")
                data = data.select_dtypes(include=[np.number])
            
            # Handle missing values
            if data.isnull().any().any():
                logger.warning("Found missing values in data, filling with 0")
                data = data.fillna(0)
            
            # Handle infinite values
            if np.isinf(data).any().any():
                logger.warning("Found infinite values in data, replacing with max/min")
                data = data.replace([np.inf, -np.inf], np.nan)
                data = data.fillna(data.max())
        
        return data

    def load_data(self, data_dir=DATA_DIR):
        """Load and preprocess data from directory."""
        try:
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                logger.warning(f"Created data directory: {data_dir}")
                return None
            
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            if not csv_files:
                logger.error(f"No CSV files found in {data_dir}")
                return None
            
            dataframes = []
            for file in csv_files:
                try:
                    df = pd.read_csv(os.path.join(data_dir, file))
                    dataframes.append(df)
                    logger.info(f"Successfully loaded {file}")
                except Exception as e:
                    logger.error(f"Error loading {file}: {str(e)}")
            
            if not dataframes:
                return None
            
            data = pd.concat(dataframes, ignore_index=True)
            self.feature_names = data.select_dtypes(include=[np.number]).columns.tolist()
            
            return self._validate_data(data)
        except Exception as e:
            logger.error(f"Failed to load data: {str(e)}")
            return None

    def train(self, data=None):
        """Train the anomaly detection model."""
        try:
            if data is None:
                data = self.load_data()
            
            if data is None or data.empty:
                logger.error("No valid training data available")
                return False
            
            # Split data for validation
            train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)
            
            logger.info("Training model...")
            self.pipeline.fit(train_data)
            
            # Validate model performance
            val_scores = self.pipeline.decision_function(val_data)
            threshold = np.percentile(val_scores, 5)  # 5% anomaly rate
            logger.info(f"Model trained with validation threshold: {threshold}")
            
            # Save model and scaler
            os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
            joblib.dump(self.pipeline, MODEL_PATH)
            logger.info(f"Model saved to {MODEL_PATH}")
            
            return True
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            return False

    def predict(self, new_data):
        """Predict anomalies in new data."""
        try:
            if self.pipeline is None:
                if os.path.exists(MODEL_PATH):
                    self.pipeline = joblib.load(MODEL_PATH)
                else:
                    logger.error("No trained model available")
                    return None
            
            new_data = self._validate_data(new_data)
            predictions = self.pipeline.predict(new_data)
            scores = self.pipeline.decision_function(new_data)
            
            return {
                'predictions': predictions,
                'scores': scores,
                'anomalies': np.where(predictions == -1)[0]
            }
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            return None

    def predict_file(self, file_path):
        """Predict anomalies from a CSV file."""
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None
            
            data = pd.read_csv(file_path)
            original_data = data.copy()
            
            results = self.predict(data)
            if results is None:
                return None
            
            result_df = original_data.copy()
            result_df['anomaly_score'] = results['scores']
            result_df['is_anomaly'] = results['predictions'] == -1
            
            output_file = file_path.replace('.csv', '_results.csv')
            result_df.to_csv(output_file, index=False)
            logger.info(f"Results saved to {output_file}")
            
            return result_df
        except Exception as e:
            logger.error(f"File prediction failed: {str(e)}")
            return None

# Create a singleton instance
anomaly_detector = EnhancedAnomalyDetector() 
