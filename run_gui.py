import os
import sys
from gui.main_window import main
from detector.anomaly_detector import anomaly_detector
from utils.logger import logger

if __name__ == "__main__":
    # Ensure required directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Train the model before starting GUI
    logger.info("Training model before starting GUI...")
    if not anomaly_detector.train():
        logger.error("Failed to train model. Please check your data files and try again.")
        sys.exit(1)
    
    # Start the GUI
    main() 
