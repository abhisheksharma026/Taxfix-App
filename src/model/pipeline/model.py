import os

from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from loguru import logger

from config.config import settings
from model.pipeline.preparation import process_input, process_features

def build_model():
    df = process_input()
    X, y = get_X_y(df)
    X = process_features(X)
    logger.info(f"Model training columns: {X.columns.tolist()}")
    X_train, X_test, X_inference, y_train, y_test, y_inference = split_train_test(X, y)
    model = train_model(X_train, y_train)
    f1_score = evaluate_model(model, X_test, y_test)
    save_model(model)

def get_X_y(df):
    X = df[settings.categorical_features + settings.numeric_features]
    y = df[settings.target]
    return X, y

def split_train_test(X, y, test_size=0.3, random_state=42):

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=test_size, random_state=random_state)
    X_test, X_inference, y_test, y_inference = train_test_split(X_temp, y_temp, test_size=0.5, random_state=random_state)
    return X_train, X_test, X_inference, y_train, y_test, y_inference

def train_model(X_train, y_train):
    logger.info("Training model")
    model = CatBoostClassifier(iterations=300, 
                            depth=6, 
                            learning_rate=0.05, 
                            loss_function='Logloss', 
                            cat_features=settings.categorical_features, 
                            auto_class_weights='Balanced',
                            verbose=100)

    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)  # Get report as a dictionary
    f1_score = report["weighted avg"]["f1-score"]
    logger.info(f"F1 score: {f1_score}")
    return f1_score

def save_model(model):
    os.makedirs(settings.model_dir, exist_ok=True)
    joblib.dump(model, settings.model_path)
    logger.info(f"Saving model into directory", settings.model_dir)
