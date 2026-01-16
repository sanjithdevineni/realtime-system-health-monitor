from typing import List
import time

from app.models import ServiceMetric, Alert, ServiceStatusValue

# Thresholds
HIGH_CPU_THRESHOLD = 85.0 # percent
HIGH_ERROR_RATE_THRESHOLD = 0.10 # 10%
HEARTBEAT_TIMEOUT_SECONDS = 5.0 # seconds

def classify_service(metric: ServiceMetric) -> ServiceStatusValue:
    """
    Decide whether a service is HEALTHY, DEGRADED, or DOWN based on its metrics.
    Priority:
    - DOWN if heartbeat is too old
    - DEGRADED if CPU or error_rate are high
    - Otherwise HEALTHY
    """
    now = time.time()
    time_since_heartbeat = now - metric.last_heartbeat

    if time_since_heartbeat > HEARTBEAT_TIMEOUT_SECONDS:
        return "DOWN"

    if metric.cpu > HIGH_CPU_THRESHOLD or metric.error_rate > HIGH_ERROR_RATE_THRESHOLD:
        return "DEGRADED"

    return "HEALTHY"

def evaluate_alerts(metrics: List[ServiceMetric]) -> List[Alert]:
    """
    Produce a list of alerts based on the current metric for all services.
    A service can have multiple alerts at once (e.g. high CPU and high errors).
    """
    now = time.time()
    alerts: List[Alert] = []

    for metric in metrics:
        time_since_heartbeat = now - metric.last_heartbeat

        if time_since_heartbeat > HEARTBEAT_TIMEOUT_SECONDS:
            alerts.append(
                Alert(
                    service_name = metric.service_name,
                    type = "SERVICE_DOWN",
                    message = f"{metric.service_name} has not sent a heartbeat for {time_since_heartbeat:.1f} seconds.",
                    severity = "CRITICAL"
                )
            )

        if metric.cpu > HIGH_CPU_THRESHOLD:
            alerts.append(
                Alert(
                    service_name = metric.service_name,
                    type = "HIGH_CPU",
                    message = f"{metric.service_name} CPU at {metric.cpu:.1f}%.",
                    severity = "WARNING"
                )
            )

        if metric.error_rate > HIGH_ERROR_RATE_THRESHOLD:
            alerts.append(
                Alert(
                    service_name = metric.service_name,
                    type = "HIGH_ERROR_RATE",
                    message = f"{metric.service_name} error rate at {metric.error_rate:.2f}.",
                    severity = "WARNING"
                )
            )
    return alerts