import pandas as pd
import joblib
from loguru import logger
from pathlib import Path
from catboost import Pool

from model import build_model
from config import settings
from preparation import process_features

class ModelService:
    def __init__(self):
        self.model = None
    
    def load_model(self, model_name=settings.model_filename):
        model_path = Path(settings.model_path)
        if not model_path.exists():
            logger.info(f"Model {model_name} not found")
            build_model()
            logger.info(f"Model {model_name} trained and saved")
            print(f"Model {model_name} trained and saved at {model_path}")

        self.model = joblib.load(settings.model_path)

    def predict(self, X):
        if self.model is None:
            self.load_model()

        if isinstance(X, dict):
            X = pd.DataFrame([X])

        X = process_features(X)
        expected_features = self.model.feature_names_
        X = X[expected_features]
    
        for col in settings.categorical_features:
            if col in X.columns:
                X[col] = X[col].astype(str)

        X_pool = Pool(X, cat_features=settings.categorical_features)
        
        return self.model.predict(X_pool)