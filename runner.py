from model_service import ModelService
from config import settings
import pandas as pd
from loguru import logger
import json
from preparation import process_features

logger.add('app.log', rotation='1 MB', level='INFO', backtrace=True, diagnose=True)

@logger.catch
def main():
    logger.info("Starting model service")
    ml_svc = ModelService()
    ml_svc.load_model()
    pred = ml_svc.predict(pd.DataFrame(process_features([settings.test_data])))
    logger.info(f"Prediction on test data from config: {pred}")

    with open('test_input.json', 'r') as f:
        test_data = json.load(f)
    test_json = pd.DataFrame([test_data])
    test_df = process_features(test_json)
    for feature in settings.categorical_features:
        test_json[feature] = test_json[feature].astype(str)
    pred = ml_svc.predict(test_json)
    logger.info(f"Prediction on test json: {pred}")
    
if __name__ == "__main__":
    main()