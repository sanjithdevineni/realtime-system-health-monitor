# Real-Time System Health Monitor

A small demo project that simulates multiple services in a distributed system and monitors their health in real time.  
The system collects metrics (CPU, memory, latency, error rate, heartbeat), evaluates alert rules, and streams updates to a live dashboard.

This project was built to practice system design, observability, and reliability concepts in a realistic, end-to-end setup.

---

## Features

- Simulated microservices emitting health metrics at regular intervals.
- Central monitoring service that:
  - Aggregates metrics.
  - Computes per-service health status.
  - Detects anomalies and failures using simple alert rules.
- Real-time dashboard that:
  - Shows current metrics for each service.
  - Highlights active alerts (high CPU, high error rate, service down).
- Clean, modular Python implementation suitable for interview walkthroughs.

---

## Tech Stack

- **Language:** Python
- **Backend:** FastAPI
- **Realtime:** WebSockets
- **Dashboard:** React
- **Server:** Uvicorn
- **Environment:** `venv` + `pip`

---

## Architecture Overview

At a high level, the system consists of:

1. **Service Simulators**  
   Simulated microservices (e.g., `auth-service`, `payment-service`) generate metrics like CPU, memory, latency, error rate, and a heartbeat timestamp.

2. **Monitoring / Collector Service**  
   A FastAPI app that receives metrics, maintains the latest state for each service, evaluates alert rules, and streams updates to connected dashboard clients over a WebSocket endpoint.

3. **Alerting Engine**  
   Evaluates simple threshold-based rules (e.g., CPU spikes, missing heartbeat) and tags services as `HEALTHY`, `DEGRADED`, or `DOWN`.

4. **Dashboard UI**  
   A lightweight UI that connects to the WebSocket endpoint and renders:
   - Per-service status cards.
   - Current metrics.
   - A list of active alerts.

> See [`PLAN.md`](./PLAN.md) for more detailed design notes and milestones.

---

## Getting Started

### Prerequisites

- Python 3.10+ (adjust as needed)
- `pip` and `venv` (or your preferred environment manager)

### Setup

```bash
# Clone the repository
git clone https://github.com/sanjithdevineni/realtime-system-health-monitor.git
cd realtime-system-health-monitor

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
