from typing import List, Literal
from pydantic import BaseModel
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.models import ServiceMetric, ServiceHealth, SystemSnapshot
from app.state import init_metrics, get_all_metrics, touch_heartbeat
from app.simulators import simulate_services
from app.alerts import classify_service, evaluate_alerts
from app.faults import set_fault, clear_fault


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def build_snapshot() -> SystemSnapshot:
    """
    Build a SystemSnapshot from the current in-memory metrics.

    - Fetches all ServiceMetric objects.
    - Classifies each service into HEALTHY / DEGRADED / DOWN.
    - Evaluates all active alerts.
    """
    metrics = get_all_metrics()

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

    alerts = evaluate_alerts(metrics)

    return SystemSnapshot(
        services = services,
        alerts = alerts
        )

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
    return build_snapshot()

@app.websocket("/ws/snapshot")
async def websocket_snapshot(websocket: WebSocket):
    """
    WebSocket endpoint that streams SystemSnapshot objects
    to the client once per second.
    """
    await websocket.accept()
    try:
        while True:
            snapshot = build_snapshot()

            payload = snapshot.model_dump()

            await websocket.send_json(payload)
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        # Client disconnected; nothing to do
        print("WebSocket client disconnected")

class FaultRequest(BaseModel):
    mode: Literal["NONE", "HIGH_CPU", "HIGH_ERROR_RATE", "DOWN"]

@app.post("/faults/{service_name}")
def set_service_fault(service_name: str, req: FaultRequest):
    if req.mode == "NONE":
        clear_fault(service_name)
        touch_heartbeat(service_name) # this is to 'kick' the service back up
    else:
        set_fault(service_name, req.mode)
    return {"service_name": service_name, "mode": req.mode}