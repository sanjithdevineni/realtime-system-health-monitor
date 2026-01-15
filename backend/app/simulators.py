"""
Responsibilities:
Loop forever (until app stops).
For each service, generate new metrics with some randomness.
Use update_metric() from state.py.
"""

import asyncio
import random
import time

from app.models import ServiceMetric
from app.state import SERVICE_NAMES, update_metric

async def simulate_services(update_interval: float = 1.0) -> None:
    """
    Periodically update metrics for each simulated service.
    This runs in an infinite loop until the application shuts down.
    """
    while True:
        now = time.time()

        for name in SERVICE_NAMES:
            # Random-ish values in reasonable ranges
            cpu = random.uniform(5.0, 95.0)
            memory = random.uniform(5.0, 95.0)
            latency_ms = random.uniform(20.0, 500.0)
            error_rate = random.uniform(0.0, 0.2)

            metric = ServiceMetric(
                service_name = name,
                cpu = cpu,
                memory = memory,
                latency_ms = latency_ms,
                error_rate = error_rate,
                last_heartbeat = now
            )

            update_metric(name, metric)

        await asyncio.sleep(update_interval)