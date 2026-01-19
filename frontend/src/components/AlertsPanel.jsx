export default function AlertsPanel({ alerts }) {
    if (!alerts || alerts.length === 0) {
        return <p>No active alerts.</p>;
    }

    return (
        <ul>
            {alerts.map((a, idx) => (
                <li key={`${a.service_name}-${a.type}-${idx}`}>
                    <b>{a.severity}</b> - {a.service_name}: {a.type} - {a.message}
                </li>
            ))}
        </ul>
    );
}