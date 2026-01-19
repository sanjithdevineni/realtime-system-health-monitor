export default function ServiceCard({ service }) {
    const { service_name, status, cpu, memory, latency_ms, error_rate } = service;
    return (
        <div style={{ border: "1px solid #333", borderRadius: 10, padding: 12 }}>
            <h3 style={{ margin: 0 }}>{service_name}</h3>
            <p style={{ margin: "6px 0" }}>
                Status: <b>{status}</b>
            </p>
            <p style={{ margin: "6px 0" }}>CPU: {Number(cpu).toFixed(1)}%</p>
            <p style={{ margin: "6px 0" }}>Memory: {Number(memory).toFixed(1)}%</p>
            <p style={{ margin: "6px 0" }}>Latency: {Number(latency_ms).toFixed(1)} ms</p>
            <p style={{ margin: "6px 0" }}>Error rate: {Number(error_rate).toFixed(2)}</p>
        </div>
    );
}