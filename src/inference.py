"""
This module defines an API using FastAPI for performing tax filing predictions.
It loads a pre-trained machine learning model and processes user input data
before making predictions.

Endpoints:
    - GET "/": Returns a welcome message.
    - GET "/health": Health check endpoint.
    - POST "/predict": Accepts user input, processes it, and returns a prediction.

Functions:
    - load_model(): Loads the pre-trained tax filing prediction model.
    - process_input(data: TaxFilingInput): Prepares input data for the model.
    - read_root(): Returns a welcome message for the API.
    - health_check(): Checks if the API is running.
    - predict(input_data: TaxFilingInput): Processes input data and returns a prediction.

Classes:
    - TaxFilingInput: Defines the expected input schema with constraints using Pydantic.
"""

import joblib

from pydantic import BaseModel, conint, confloat, constr
import pandas as pd
from loguru import logger
from fastapi import FastAPI, HTTPException

from src.config.config import settings
from src.model.pipeline.preparation import process_features

app = FastAPI()
# To test inference API
# poetry run uvicorn src.inference:app --reload
# curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d @test_input.json


def load_model():
    """
    Load the pre-trained tax filing prediction model.

    Returns:
        model: The trained machine learning model.

    Raises:
        HTTPException: If the model fails to load.
    """

    try:
        model = joblib.load(settings.model_path)
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail="Model loading failed")

    return joblib.load(settings.model_path)


class TaxFilingInput(BaseModel):
    """
    Defines the expected input schema for tax filing predictions.

    Attributes:
        age (int): Age of the user (between 18 and 100).
        income (float): Non-negative income value.
        employment_type (str): Type of employment (e.g., full-time, part-time).
        marital_status (str): Marital status of the user.
        time_spent_on_platform (float): Time spent on the platform in minutes.
        number_of_sessions (int): Number of user sessions.
        fields_filled_percentage (float): Percentage of form fields completed (0-100).
        previous_year_filing (int): Binary flag indicating prior tax filing (0 or 1).
        device_type (str): Type of device used (e.g., mobile, desktop).
        referral_source (str): Source of referral (e.g., friend, ad).
    """

    age: conint(ge=18, le=100) = 30  # Age between 18 and 100
    income: confloat(ge=0) = 50000  # Non-negative income
    employment_type: constr(strip_whitespace=True) = "full-time"
    marital_status: constr(strip_whitespace=True) = "single"
    time_spent_on_platform: confloat(ge=0) = 120.5
    number_of_sessions: conint(ge=0) = 10
    fields_filled_percentage: confloat(ge=0, le=100) = 80.0  # Percentage 0-100
    previous_year_filing: conint(ge=0, le=1) = 1  # Binary
    device_type: constr(strip_whitespace=True) = "mobile"
    referral_source: constr(strip_whitespace=True) = "friend"

    class Config:
        schema_extra = {
            "example": {
                "age": 30,
                "income": 50000,
                "employment_type": "full-time",
                "marital_status": "single",
                "time_spent_on_platform": 120.5,
                "number_of_sessions": 10,
                "fields_filled_percentage": 80.0,
                "previous_year_filing": 1,
                "device_type": "mobile",
                "referral_source": "friend",
            }
        }


def process_input(data: TaxFilingInput):
    """
    Process user input data before feeding it into the model.

    Args:
        data (TaxFilingInput): Input data from the user.

    Returns:
        pd.DataFrame: Processed input data as a DataFrame.
    """
    df = pd.DataFrame([data.model_dump()])
    df = process_features(df)
    # logger.info(f"Processed input data")
    return df


@app.get("/")
async def read_root():
    """
    Root endpoint to confirm API is running.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the TaxFix API"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: API status message.
    """
    return {"status": "API is running"}


# Prediction endpoint
@app.post("/predict")
async def predict(input_data: TaxFilingInput):
    """
    Endpoint to make a tax filing prediction.

    Args:
        input_data (TaxFilingInput): The structured user input.

    Returns:
        dict: The predicted tax filing completion status.

    Raises:
        HTTPException: If prediction fails due to processing errors.
    """
    try:
        processed_input = process_input(input_data)
        model = load_model()
        expected_features = model.feature_names_
        processed_input = processed_input[expected_features]
        prediction = model.predict(processed_input)[0]
        return {"completed_filing": int(prediction)}
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")
