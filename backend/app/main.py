from typing import List
import asyncio

from fastapi import FastAPI

from app.models import ServiceMetric, ServiceHealth, SystemSnapshot
from app.state import init_metrics, get_all_metrics
from app.simulators import simulate_services
from app.alerts import classify_service, evaluate_alerts


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

@app.get("/snapshot", response_model=SystemSnapshot)
def get_snapshot():
    """
    Return a combined view of the system:
    - services: metrics + computed status for each service
    - alerts: list of active alerts across all services
    """
    metrics = get_all_metrics()

    # Build per-service health objects (metrics + status)
    services: List[ServiceHealth] = []
    for metric in metrics:
        status = classify_service(metric)
        services.append(
            ServiceHealth(
                service_name = metric.service_name,
                cpu = metric.cpu,
                memory = metric.memory,
                latency_ms = metric.latency_ms,
                error_rate = metric.error_rate,
                last_heartbeat = metric.last_heartbeat,
                status = status
            )
        )
    
    # Evaluate alerts based on current metrics
    alerts = evaluate_alerts(metrics)

    return SystemSnapshot(
        services = services,
        alerts = alerts
    )