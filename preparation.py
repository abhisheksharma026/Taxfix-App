import pandas as pd
from collection import load_data, load_data_from_db

def process_input():
    df = load_data_from_db()
    df["sessions_per_minute"] = df["number_of_sessions"] / (df["time_spent_on_platform"] + 1)
    df["fields_filled_x_sessions"] = df["fields_filled_percentage"] * df["number_of_sessions"]
    
    return df

def process_features(X):
    if isinstance(X, list):
        X = pd.DataFrame(X)
    X['age'] = X['age'].astype(int)
    X['income'] = X['income'].astype(float)
    X['employment_type'] = X['employment_type'].astype(str)
    X['marital_status'] = X['marital_status'].astype(str)
    X['time_spent_on_platform'] = X['time_spent_on_platform'].astype(float)
    X['number_of_sessions'] = X['number_of_sessions'].astype(int)
    X['fields_filled_percentage'] = X['fields_filled_percentage'].astype(float)
    X['previous_year_filing'] = X['previous_year_filing'].astype(int).astype(str)
    X['device_type'] = X['device_type'].astype(str)
    X['referral_source'] = X['referral_source'].astype(str)
    X["sessions_per_minute"] = X["number_of_sessions"] / (X["time_spent_on_platform"] + 1)
    X["fields_filled_x_sessions"] = X["fields_filled_percentage"] * X["number_of_sessions"]
    X["sessions_per_minute"] = X["sessions_per_minute"].astype(float).astype(int)
    X["fields_filled_x_sessions"] = X["fields_filled_x_sessions"].astype(float).astype(int)
    
    return X