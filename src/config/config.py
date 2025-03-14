"""
This module defines configuration settings for the application.
It uses Pydantic for structured settings and SQLAlchemy
for database connectivity.

Classes:
    Settings: Defines configuration parameters for model paths, feature lists,
              database connection, and test data.

Variables:
    settings (Settings): An instance of the Settings class, preloaded with default values.
    engine (sqlalchemy.Engine): SQLAlchemy engine initialized with the database connection string.
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath
from sqlalchemy import create_engine


class Settings(BaseSettings):
    """
    Configuration settings for the TaxFix application.

    Attributes:
        model_config (SettingsConfigDict): Configuration for loading environment variables.
        model_dir (DirectoryPath): Directory path where models are stored.
        model_filename (str): Name of the machine learning model file.
        model_path (str): Full path to the saved machine learning model.
        data_path (str): Path to the dataset CSV file.
        categorical_features (list): List of categorical feature column names.
        numeric_features (list): List of numerical feature column names.
        target (str): Name of the target variable for prediction.
        test_data (dict): Sample test data for inference.
        db_conn_str (str): Database connection string.
        table_name (str): Name of the database table used for storage.
    """

    model_config = SettingsConfigDict(env_file="config/.env", env_file_encoding="utf-8")
    model_dir: DirectoryPath = "src/model/models"
    model_filename: str = "catboost_model_v1.pkl"
    model_path: str = os.path.join(model_dir, model_filename)
    data_path: str = "data/dataset.csv"
    categorical_features: list = [
        "employment_type",
        "marital_status",
        "device_type",
        "referral_source",
        "previous_year_filing",
    ]
    numeric_features: list = [
        "age",
        "income",
        "time_spent_on_platform",
        "number_of_sessions",
        "fields_filled_percentage",
        "sessions_per_minute",
        "fields_filled_x_sessions",
    ]
    target: str = "completed_filing"
    test_data: dict = {
        "age": 30,
        "income": 45000,
        "employment_type": "full_time",
        "marital_status": "single",
        "time_spent_on_platform": 120,
        "number_of_sessions": 5,
        "fields_filled_percentage": 80,
        "previous_year_filing": 1,
        "device_type": "mobile",
        "referral_source": "friend_referral",
    }
    db_conn_str: str = "sqlite:///db.sqlite"
    table_name: str = "dataset"


settings = Settings()
engine = create_engine(settings.db_conn_str)
