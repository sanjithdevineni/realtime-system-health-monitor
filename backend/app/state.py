# Define a fixed list of service names
# Keep a dict: service_name -> ServiceMetric
# provide helpers to:
# - initialize metrics
# - update metrics
# - read all metrics

from typing import Dict, List, Optional
import time
from app.models import ServiceMetric

# For now we hard-code the services we want to simulate.
SERVICE_NAMES = [
    "auth-service",
    "payment-service",
    "reporting-service",
]

# In-memory store: service_name -> latest metrics
_metrics_by_service: Dict[str, ServiceMetric] = {}

def touch_heartbeat(service_name: str) -> bool:
    """
    Force-update last_heartbeat to 'now' for a service if it exists.
    Returns True if the service existed and and was updated.
    """
    metric = _metrics_by_service.get(service_name)
    if metric is None:
        return False
    metric.last_heartbeat = time.time()
    _metrics_by_service[service_name] = metric
    return True

def init_metrics() -> None:
    """
    Initialize the in-memory metrics for each service with some default values.
    """
    global _metrics_by_service
    now = time.time()
    _metrics_by_service = {
        name: ServiceMetric(
            service_name = name,
            cpu = 0.0,
            memory = 0.0,
            latency_ms = 0.0,
            error_rate = 0.0,
            last_heartbeat = now,
        )
        for name in SERVICE_NAMES

    }

def update_metric(service_name: str, metric: ServiceMetric) -> None:
    """
    Update the metrics for a given service.
    """
    _metrics_by_service[service_name] = metric

def get_all_metrics() -> List[ServiceMetric]:
    """
    Return the current metrics for all services as a List.
    """
    return list(_metrics_by_service.values())