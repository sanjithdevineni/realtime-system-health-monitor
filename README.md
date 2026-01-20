# Real-Time System Health Monitor

A demo project that simulates multiple services in a distributed system and monitors their health in real time.  
Simulated microservices emit metrics (CPU, memory, latency, error rate, heartbeat). A central FastAPI backend aggregates metrics, evaluates alert rules, and exposes both HTTP and WebSocket endpoints. A React (Vite) frontend renders a live dashboard.

This project is meant to demonstrate end-to-end system design, observability, and reliability in a presentation-ready, understandable implementation.

---

## Features

- Simulated microservices emitting health metrics at regular intervals.
- FastAPI monitoring service that aggregates metrics, computes per-service health, and evaluates alert rules.
- WebSocket streaming of aggregated metrics and active alerts.
- React dashboard with real-time service status and alert highlights.
- Clean, modular implementation suitable for walkthroughs.

---

## Tech Stack

- **Backend:** Python, FastAPI, Pydantic, Uvicorn
- **Frontend:** React + Vite
- **Realtime:** WebSockets (FastAPI WebSocket endpoint + browser WebSocket client)
- **Environment:** `venv` + `pip`

---

## Repo Structure (Approximate)

```
realtime-system-health-monitor/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ models.py
│  │  ├─ simulators.py
│  │  ├─ state.py
│  │  └─ alerts.py
│  └─ requirements.txt
├─ frontend/
│  ├─ package.json
│  └─ src/
│     ├─ App.(t|j)sx
│     ├─ components/
│     └─ hooks/
├─ docs/
│  └─ PLAN.md
└─ README.md
```

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
   A React (Vite) UI that connects to the WebSocket endpoint and renders:
   - Per-service status cards.
   - Current metrics.
   - A list of active alerts.

> See [`docs/PLAN.md`](./docs/PLAN.md) for more detailed design notes and milestones.

---

## Getting Started

### Prerequisites

- Python 3.10+ (adjust as needed)
- `pip` and `venv` (or your preferred environment manager)
- Node.js 18+ and npm (for the React frontend)

### Setup

```bash
# Clone the repository
git clone https://github.com/sanjithdevineni/realtime-system-health-monitor.git
cd realtime-system-health-monitor
```

### Backend (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```
