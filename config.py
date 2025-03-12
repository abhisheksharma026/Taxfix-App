import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath
from sqlalchemy import create_engine

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    model_dir: DirectoryPath = "models"
    model_filename: str = "catboost_model_v1.pkl"
    model_path: str = os.path.join(model_dir, model_filename)
    data_path: str = "data/dataset.csv"
    categorical_features: list = ["employment_type", 
                                  "marital_status", 
                                  "device_type", 
                                  "referral_source", 
                                  "previous_year_filing"]
    numeric_features: list = ["age", 
                             "income", 
                             "time_spent_on_platform", 
                             "number_of_sessions", 
                             "fields_filled_percentage", 
                             "sessions_per_minute", 
                             "fields_filled_x_sessions"]
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
    "referral_source": "friend_referral"
    }
    db_conn_str: str = "sqlite:///db.sqlite"
    table_name: str = "dataset"

settings = Settings()
engine = create_engine(settings.db_conn_str)