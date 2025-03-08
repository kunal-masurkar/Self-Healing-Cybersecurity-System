import os
import pandas as pd
import numpy as np
import importlib.util
import sys

# Project root directory
project_dir = os.path.abspath('.')

# Load test data
print("Loading test data...")
test_data_path = os.path.join(project_dir, 'data', 'test_data.csv')
test_data = pd.read_csv(test_data_path)

# Find Python files that might contain the model implementation
python_files = []
for root, dirs, files in os.walk(project_dir):
    for file in files:
        if file.endswith('.py') and file not in ['check.py']:
            python_files.append(os.path.join(root, file))

print(f"\nFound {len(python_files)} Python files in the project:")
for file in python_files:
    print(f"- {os.path.relpath(file, project_dir)}")

# Function to analyze a Python file
def analyze_py_file(file_path):
    print(f"\nAnalyzing {os.path.basename(file_path)}...")
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Look for model-related keywords
    keywords = [
        'predict', 'model', 'classifier', 'detect', 'anomaly', 
        'threat', 'attack', 'malicious', 'sklearn', 'tensorflow',
        'accuracy', 'precision', 'recall', 'f1', 'score'
    ]
    
    findings = {}
    for keyword in keywords:
        count = content.lower().count(keyword)
        if count > 0:
            findings[keyword] = count
    
    if findings:
        print("Keywords found:")
        for keyword, count in findings.items():
            print(f"- '{keyword}': {count} occurrences")
    else:
        print("No relevant keywords found.")

# Try to import and analyze main modules
def try_import_module(file_path):
    try:
        module_name = os.path.basename(file_path).replace('.py', '')
        
        # Add directory to path
        sys.path.insert(0, os.path.dirname(file_path))
        
        # Import the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Look for prediction or detection functions
        prediction_funcs = []
        for name in dir(module):
            attr = getattr(module, name)
            if callable(attr) and any(keyword in name.lower() for keyword in 
                                      ['predict', 'detect', 'classify', 'score', 'evaluate']):
                prediction_funcs.append(name)
        
        if prediction_funcs:
            print(f"Found potential prediction/detection functions: {prediction_funcs}")
            return module, prediction_funcs
        else:
            print("No prediction/detection functions found.")
            return module, []
    
    except Exception as e:
        print(f"Error importing module: {str(e)}")
        return None, []

# Analyze each Python file
for file_path in python_files:
    analyze_py_file(file_path)

# Try to import main modules
main_module_paths = [
    os.path.join(project_dir, 'detector.py'),
    os.path.join(project_dir, 'main.py'),
    os.path.join(project_dir, 'firewall.py')
]

for path in main_module_paths:
    if os.path.exists(path):
        print(f"\nTrying to import and analyze {os.path.basename(path)}...")
        module, funcs = try_import_module(path)