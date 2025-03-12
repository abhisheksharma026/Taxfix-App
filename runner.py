"""
This module serves as the entry point for executing the TaxFix model service.
It loads the trained model, processes test input data, makes predictions, 
and logs the results.

Functions:
    - main(): Loads the model, makes predictions on test data, and logs results.
"""

import json

import pandas as pd
from loguru import logger

from model_service import ModelService
from config import settings
from preparation import process_features

logger.add('app.log', rotation='1 MB', level='INFO', backtrace=True, diagnose=True)

@logger.catch
def main():
    """
    Main function to run the model service.

    This function:
    1. Loads the trained machine learning model.
    2. Makes predictions on test data from the `settings` file.
    3. Loads test input from `test_input.json`, processes it, and makes predictions.
    4. Logs predictions for both test cases.

    Raises:
        Exception: Catches and logs any runtime errors.
    """

    logger.info("Starting model service")
    ml_svc = ModelService()
    ml_svc.load_model()
    pred_test = ml_svc.predict(pd.DataFrame(process_features([settings.test_data])))
    logger.info(f"Prediction on test data from config: {pred_test}")

    with open('test_input.json', 'r') as f:
        test_data = json.load(f)
    test_json = pd.DataFrame([test_data])
    test_json = process_features(test_json)
    pred_json = ml_svc.predict(test_json)
    logger.info(f"Prediction on test json: {pred_json}")
    
if __name__ == "__main__":
    main()