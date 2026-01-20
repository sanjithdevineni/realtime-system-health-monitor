import { useState } from "react";

export default function ServiceCard({ service }) {
  if (!service) return null;

  const { service_name, status, cpu, memory, latency_ms, error_rate } = service;
  const isDown = status === "DOWN";

  const [busy, setBusy] = useState(false);

  async function setFault(mode) {
    try {
      setBusy(true);
      const res = await fetch(`http://127.0.0.1:8000/faults/${service_name}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode }),
      });

      if (!res.ok) {
        console.error("Fault request failed:", res.status);
      }
    } catch (err) {
      console.error("Fault request error:", err);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div style={{ border: "1px solid #333", borderRadius: 10, padding: 12 }}>
      <h3 style={{ margin: 0 }}>{service_name}</h3>

      <p style={{ margin: "6px 0" }}>
        Status: <b>{status}</b>
      </p>

      <p style={{ margin: "6px 0" }}>
        CPU: {isDown ? "N/A (stale)" : `${Number(cpu).toFixed(1)}%`}
      </p>

      <p style={{ margin: "6px 0" }}>
        Memory: {isDown ? "N/A (stale)" : `${Number(memory).toFixed(1)}%`}
      </p>

      <p style={{ margin: "6px 0" }}>
        Latency: {isDown ? "N/A (stale)" : `${Number(latency_ms).toFixed(1)} ms`}
      </p>

      <p style={{ margin: "6px 0" }}>
        Error rate: {isDown ? "N/A (stale)" : Number(error_rate).toFixed(2)}
      </p>

      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 10 }}>
        <button
          disabled={busy}
          onClick={(e) => {
            setFault("HIGH_CPU");
            e.currentTarget.blur();
          }}
        >
          High CPU
        </button>

        <button
          disabled={busy}
          onClick={(e) => {
            setFault("HIGH_ERROR_RATE");
            e.currentTarget.blur();
          }}
        >
          High Error
        </button>

        <button
          disabled={busy}
          onClick={(e) => {
            setFault("DOWN");
            e.currentTarget.blur();
          }}
        >
          Down
        </button>

        <button
          disabled={busy}
          onClick={(e) => {
            setFault("NONE");
            e.currentTarget.blur();
          }}
        >
          Clear
        </button>
      </div>
    </div>
  );
}