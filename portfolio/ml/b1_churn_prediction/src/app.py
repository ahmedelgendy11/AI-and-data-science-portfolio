# -*- coding: utf-8 -*-
"""
Churn Prediction API — FastAPI service that serves the trained pipeline.
Run:  uvicorn app:app --reload   (from inside the src/ folder)
Docs: http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "churn_model.joblib")

app = FastAPI(title="Customer Churn Prediction API", version="1.0")
model = None


class Customer(BaseModel):
    recency: int
    tenure: int
    frequency: int
    monetary: float
    avg_order_value: float
    total_items: int
    n_categories: int
    main_country: str
    main_payment: str


@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)


@app.get("/")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict")
def predict(customer: Customer, threshold: float = 0.5):
    if model is None:
        return {"error": "Model not loaded. Train it in the notebook first (cell 8)."}
    X = pd.DataFrame([customer.dict()])
    proba = float(model.predict_proba(X)[0, 1])
    return {
        "churn_probability": round(proba, 4),
        "will_churn": bool(proba >= threshold),
        "threshold": threshold,
        "recommended_action": (
            "Target with retention offer" if proba >= threshold else "No action needed"
        ),
    }
