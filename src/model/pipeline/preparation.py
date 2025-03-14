"""
This module provides functions for preprocessing input data.
It includes functions to load data, process database records, and apply feature
engineering transformations.

Functions:
    - process_input(): Loads and processes data from the database.
    - process_features(X): Prepares and transforms input features for the model.
"""

import pandas as pd
from src.model.pipeline.collection import load_data  # , load_data_from_db


def process_input():
    """
    Loads data from the database and applies feature engineering transformations.

    Returns:
        pd.DataFrame: A DataFrame containing processed user data with additional features.
    """
    df = load_data()
    df["sessions_per_minute"] = df["number_of_sessions"] / (
        df["time_spent_on_platform"] + 1
    )
    df["fields_filled_x_sessions"] = (
        df["fields_filled_percentage"] * df["number_of_sessions"]
    )

    return df


def process_features(X):
    """
    Processes input data by converting data types and applying feature transformations.

    Args:
        X (list or pd.DataFrame): The input data to be processed. If a list is provided,
        it is converted to a DataFrame.

    Returns:
        pd.DataFrame: The transformed DataFrame with appropriate feature types and
        engineered features.
    """

    if isinstance(X, list):
        X = pd.DataFrame(X)
    X["age"] = X["age"].astype(int)
    X["income"] = X["income"].astype(float)
    X["employment_type"] = X["employment_type"].astype(str)
    X["marital_status"] = X["marital_status"].astype(str)
    X["time_spent_on_platform"] = X["time_spent_on_platform"].astype(float)
    X["number_of_sessions"] = X["number_of_sessions"].astype(int)
    X["fields_filled_percentage"] = X["fields_filled_percentage"].astype(float)
    X["previous_year_filing"] = X["previous_year_filing"].astype(int).astype(str)
    X["device_type"] = X["device_type"].astype(str)
    X["referral_source"] = X["referral_source"].astype(str)
    X["sessions_per_minute"] = X["number_of_sessions"] / (
        X["time_spent_on_platform"] + 1
    )
    X["fields_filled_x_sessions"] = (
        X["fields_filled_percentage"] * X["number_of_sessions"]
    )
    X["sessions_per_minute"] = X["sessions_per_minute"].astype(float).astype(int)
    X["fields_filled_x_sessions"] = (
        X["fields_filled_x_sessions"].astype(float).astype(int)
    )

    return X
