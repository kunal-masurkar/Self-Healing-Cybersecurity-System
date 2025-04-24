import os
import sys
from config import DATA_DIR, MODEL_PATH
from detector.anomaly_detector import anomaly_detector
from security.response import security_response
from utils.logger import logger

def main():
    try:
        # Train the model with sample data
        logger.info("Starting the anomaly detection system...")
        
        # Force training with sample data
        logger.info("Training the model with sample data...")
        if not anomaly_detector.train():
            logger.error("Failed to train model. Exiting.")
            sys.exit(1)
        
        # Load and preprocess test data
        logger.info("Loading test data...")
        test_data = anomaly_detector.load_data()
        if test_data is None:
            logger.error("No test data available. Exiting.")
            sys.exit(1)

        # Predict anomalies
        logger.info("Analyzing network traffic for anomalies...")
        results = anomaly_detector.predict(test_data)
        if results is None:
            logger.error("Prediction failed. Exiting.")
            sys.exit(1)

        # Process anomalies
        for idx in results['anomalies']:
            # Simulate malicious IP (in real scenario, this would come from the data)
            malicious_ip = f"192.168.1.{100 + idx}"
            
            try:
                # Block the IP with a reason
                security_response.block_ip(
                    malicious_ip,
                    reason=f"Anomaly detected in row {idx} with score {results['scores'][idx]:.2f}"
                )
                
                logger.info(f"Successfully processed threat from IP {malicious_ip}")
            except Exception as e:
                logger.error(f"Failed to process threat from IP {malicious_ip}: {str(e)}")

        # Print summary
        total_anomalies = len(results['anomalies'])
        logger.info(f"Analysis complete. Found {total_anomalies} anomalies.")
        
        if total_anomalies > 0:
            logger.info("Blocked IPs:")
            for ip, info in security_response.get_blocked_ips().items():
                logger.info(f"- {ip} (Blocked at: {info['block_time']}, Reason: {info['reason']})")
        else:
            logger.info("No anomalies detected in this analysis.")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
