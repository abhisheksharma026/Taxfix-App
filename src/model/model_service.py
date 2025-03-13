"""
This module provides the ModelService class, which handles loading and making 
predictions using a CatBoost model. If the model is not found, it is automatically 
trained and saved.

Classes:
    - ModelService: Handles model loading, inference, and preprocessing.

Functions:
    - load_model(): Loads the trained CatBoost model from a file.
    - predict(X): Processes input data and returns model predictions.
"""

import pandas as pd
import joblib
from loguru import logger
from pathlib import Path
from catboost import Pool

from model.pipeline.model import build_model
from config.config import settings
from model.pipeline.preparation import process_features

class ModelService:
    """
    A service class for managing the machine learning model lifecycle, including 
    loading, training (if needed), and making predictions.

    Attributes:
        model (CatBoostClassifier or None): The trained CatBoost model.
    """

    def __init__(self):
        """
        Initializes the ModelService instance without loading the model initially.
        """
        self.model = None
    
    def load_model(self, model_name=settings.model_filename):
        """
        Loads the trained CatBoost model from disk. If the model is not found, 
        it triggers training using `build_model()`.

        Args:
            model_name (str, optional): The name of the model file. 
                                        Defaults to `settings.model_filename`.

        Raises:
            FileNotFoundError: If the model file is missing and cannot be built.
        """

        model_path = Path(settings.model_path)
        if not model_path.exists():
            logger.info(f"Model {model_name} not found")
            build_model()
            logger.info(f"Model {model_name} trained and saved")
            print(f"Model {model_name} trained and saved at {model_path}")

        self.model = joblib.load(settings.model_path)

    def predict(self, X):
        """
        Processes input data and makes predictions using the trained model.

        Args:
            X (dict or pd.DataFrame): Input features for prediction. 
                                      If a dictionary is provided, it is converted to a DataFrame.

        Returns:
            np.ndarray: Model predictions.

        Raises:
            ValueError: If input data does not match expected features.
        """
        
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