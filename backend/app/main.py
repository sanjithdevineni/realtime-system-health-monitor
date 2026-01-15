from typing import List
import asyncio

from fastapi import FastAPI

from app.models import ServiceMetric
from app.state import init_metrics, get_all_metrics
from app.simulators import simulate_services


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """
    Initialize in-memory metrics and start the simulator loop
    when the FastAPI application starts.
    """
    init_metrics()
    # Start simulators in the background
    asyncio.create_task(simulate_services())

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/metrics", response_model=List[ServiceMetric])
def get_metrics():
    """
    Return the latest metrics for all services.
    """
    return get_all_metrics()