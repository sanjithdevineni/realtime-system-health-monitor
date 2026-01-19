import { useSnapshotStream } from "./hooks/useSnapshotStream";
import ServiceCard from "./components/ServiceCard";
import AlertsPanel from "./components/AlertsPanel";

export default function App() {
  const { snapshot, connStatus } = useSnapshotStream("ws://127.0.0.1:8000/ws/snapshot");
  const { services, alerts } = snapshot;

  return (
    <div style={{ padding: 24, fontFamily: "system-ui, Arial" }}>
      <h1 style={{ marginTop: 0 }}>Real-Time System Health Monitor</h1>
      <p>
        WebSocket: <b>{connStatus}</b>
      </p>

      <h2>Services</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
          gap: 12,
        }}
      >
        {services.map((s) => (
          <ServiceCard key={s.service_name} service={s} />
        ))}
      </div>

      <h2 style={{ marginTop: 24 }}>Active Alerts</h2>
      <AlertsPanel alerts={alerts} />
    </div>
  );
}