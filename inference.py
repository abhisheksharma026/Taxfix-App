from fastapi import FastAPI, HTTPException
import joblib
import psutil
import nest_asyncio
import subprocess
from config import settings
from pydantic import BaseModel, conint, confloat, constr
import pandas as pd
from loguru import logger
from preparation import process_features

app = FastAPI()

def load_model():
    try:
        model = joblib.load(settings.model_path)
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail="Model loading failed")

    return joblib.load(settings.model_path)

class TaxFilingInput(BaseModel):
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
                "referral_source": "friend"
            }
        }

def process_input(data: TaxFilingInput):
    df = pd.DataFrame([data.model_dump()])
    df = process_features(df)
    logger.info(f"Processed input data: {df}")
    return df

@app.get("/")
async def read_root():
    return {"message": "Welcome to the TaxFix API"}

@app.get("/health")
async def health_check():
    return {"status": "API is running"}

# Prediction endpoint
@app.post("/predict")
async def predict(input_data: TaxFilingInput):
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
    
