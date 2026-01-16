from typing import Literal, List
from pydantic import BaseModel


class ServiceMetric(BaseModel):
    service_name: str
    cpu: float          # percent, 0–100
    memory: float       # percent, 0–100
    latency_ms: float
    error_rate: float   # between 0 and 1
    last_heartbeat: float  # Unix timestamp (seconds)

ServiceStatusValue = Literal["HEALTHY", "DEGRADED", "DOWN"]

class ServiceStatus(BaseModel):
    service_name: str
    status: ServiceStatusValue

class Alert(BaseModel):
    service_name: str
    type: str       # e.g. "HIGH_CPU", "SERVICE_DOWN"
    message: str
    severity: Literal["INFO", "WARNING", "CRITICAL"]

class ServiceHealth(BaseModel):
    service_name: str
    cpu: float
    memory: float
    latency_ms: float
    error_rate: float
    last_heartbeat: float
    status: ServiceStatusValue

class SystemSnapshot(BaseModel):
    services: List[ServiceHealth]
    alerts: List[Alert]