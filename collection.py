import pandas as pd
from loguru import logger
from config import settings

def load_data(path=settings.data_path):
    logger.info(f"Loading data from {path}")
    return pd.read_csv(path)
