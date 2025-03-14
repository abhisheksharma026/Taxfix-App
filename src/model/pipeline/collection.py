"""
This module provides functions to load data from a CSV file or a database
for the TaxFix application.

Functions:
    load_data(path): Loads data from a specified CSV file path.
    load_data_from_db(): Loads data from the database using SQLAlchemy.
"""

import pandas as pd
from loguru import logger
from sqlalchemy import select

from src.db.db_model import TaxFix
from src.config.config import settings, engine


def load_data(path=settings.data_path):
    """
    Load data from a CSV file.

    Args:
        path (str, optional): The file path of the CSV to load.
                              Defaults to `settings.data_path`.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the loaded data.
    """
    logger.info(f"Loading data from {path}")
    return pd.read_csv(path)


def load_data_from_db():
    """
    Load data from the database using SQLAlchemy.

    This function constructs a SQL query to fetch all records from the `TaxFix` table
    and executes it using the database engine defined in `settings`.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the retrieved data.
    """
    logger.info("Loading data from database")
    query = select(TaxFix)
    return pd.read_sql(query, engine)
