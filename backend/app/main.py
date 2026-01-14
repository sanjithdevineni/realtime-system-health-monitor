from typing import List
from fastapi import FastAPI
from app.models import ServiceMetric


app = FastAPI()

fake_metrics: List[ServiceMetric] = []

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/metrics", response_model=List[ServiceMetric])
def get_metrics():
    """
    Temporary metrics endpoint.
    For now it just returns an empty list; later it will read from state.py.
    """
    return fake_metrics