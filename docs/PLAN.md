# Real-Time System Health Monitor – Project Plan

## 1. High-Level Idea

Build a small distributed system with multiple simulated services that emit health metrics (CPU, memory, latency, error rate, heartbeat). A central FastAPI backend collects these metrics and exposes them to a real-time React dashboard via HTTP and WebSocket endpoints, which displays current system health and raises alerts when services become degraded or unresponsive.

The goal is to demonstrate end-to-end system design, reliability, and observability in a realistic but lightweight setting.

---

## 2. Goals

- Show **end-to-end ownership**: design, implementation, monitoring, and demo.
- Demonstrate **system design thinking** (services, communication, data flow).
- Practice **reliability and observability** concepts: metrics, health checks, alerts.
- Keep the scope **small enough** to implement, polish, and present clearly.
- Keep the implementation **understandable and presentation-ready**.
- Maintain **clean, professional documentation**.
- Have a clear narrative for a **5–7 slide, ~10 minute presentation**.

---

## 3. Tech Stack

- **Backend:** Python, FastAPI, Pydantic, Uvicorn
- **Frontend:** React + Vite
- **Real-Time Updates:** WebSockets (FastAPI WebSocket endpoint + browser WebSocket client)
- **Data Store:** In-memory (Python dicts / simple classes for metrics)
- **Environment:** `pip` / `venv` for dependency management

---

## 4. System Overview

### 4.1 Core Components

1. **Service Simulators**
   - 3–4 simulated microservices (e.g., `auth-service`, `payment-service`, `reporting-service`).
   - Each periodically emits metrics:
     - CPU usage
     - Memory usage
     - Request latency
     - Error rate
     - Heartbeat timestamp

2. **Monitoring / Collector Service**
   - FastAPI app that exposes:
     - HTTP endpoints for basic health/info.
     - WebSocket endpoint for streaming aggregated metrics to the dashboard.
   - Maintains the latest state per service in memory.
   - Computes derived values:
     - Rolling averages (e.g., latency over last N samples).
     - Overall service status: `HEALTHY`, `DEGRADED`, `DOWN`.

3. **Alerting Logic**
   - Threshold-based rules, e.g.:
     - CPU > 85% for N consecutive intervals → `HIGH_CPU` alert.
     - Error rate > X% → `HIGH_ERROR_RATE` alert.
     - Missing heartbeat for > T seconds → `SERVICE_DOWN` alert.
   - Produces a list of active alerts to send to the dashboard.

4. **Dashboard UI**
   - Displays per-service cards with:
     - Name
     - Status (colored badge)
     - Key metrics
   - Global view:
     - List of active alerts
     - Simple charts (e.g., latency or CPU over time) if time allows.
   - Consumes real-time updates via WebSocket using a React (Vite) client.

---

## 5. Architecture (Current)

**Data Flow:**

1. Simulated services generate metrics on an interval (e.g., every 1–2 seconds).
2. Services send metrics to the **Monitoring/Collector** (function call, internal client, or HTTP).
3. Collector updates in-memory state and evaluates **alert rules**.
4. Collector pushes updates (metrics + alerts) to connected dashboard clients via **WebSocket**.
5. Dashboard renders current system state and highlights any alerts.

---

## 6. Milestones

1. **Design & Setup**
   - Confirm FastAPI + React + Vite stack and repo structure.
   - Set up repo structure and virtual environment.
   - Define data models (metric payload, service status, alert types).

2. **Service Simulators**
   - Implement 3–4 simple services that:
     - Generate pseudo-random metrics with realistic ranges.
     - Occasionally simulate spikes or failures (e.g., stop heartbeats).

3. **Monitoring / Collector Service**
   - Implement FastAPI app:
     - In-memory store for metrics by service.
     - Functions to update metrics and recompute status.
     - WebSocket endpoint to stream updates.

4. **Alerting Logic**
   - Implement alert evaluation rules.
   - Maintain current set of active alerts.
   - Include alerts in WebSocket payload.

5. **Dashboard**
   - Implement basic React UI:
     - Service list + status.
     - Active alerts section.
   - Hook up to WebSocket for real-time updates.
   - (Optional) Add simple charts for one or two metrics.

6. **Polish & Presentation Prep**
   - Clean up code structure & comments.
   - Add `README.md` and usage instructions.
   - Prepare slides:
     - Problem → Architecture → Implementation → Demo → Lessons.
   - Run through the demo several times.

---

## 7. Possible Extensions (If Time Allows)

- Persist metrics in a lightweight database (SQLite, Redis, etc.).
- Add historical charts with simple time windows.
- Support multiple dashboard clients.
- Add different failure modes (e.g., high latency vs total outage).
- Add a configuration file for thresholds and service definitions.

---

## 8. Update Log

_Use this section to track progress and key decisions._

- [ ] Tech stack finalized (FastAPI + React + Vite).
- [ ] Repo created and initial skeleton pushed.
- [ ] Service simulators implemented.
- [ ] Monitoring/collector implemented.
- [ ] Alerting logic implemented.
- [ ] Dashboard connected to WebSocket.
- [ ] Basic styling / polish done.
- [ ] Slides created and demo rehearsed.
