import pandas as pd
from loguru import logger
from sqlalchemy import select

from db_model import TaxFix
from config import settings

def load_data(path=settings.data_path):
    logger.info(f"Loading data from {path}")
    return pd.read_csv(path)

def load_data_from_db():
    logger.info(f"Loading data from database")
    query = select(TaxFix)
    return pd.read_sql(query, settings.engine)
