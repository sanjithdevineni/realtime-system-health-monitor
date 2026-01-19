import { useEffect, useState } from "react";

export function useSnapshotStream(url) {
    const [snapshot, setSnapshot] = useState({services: [], alerts: []});
    const [connStatus, setConnStatus] = useState("DISCONNECTED"); // CONNECTING/CONNECTED/ERROR

    useEffect(() => {
        setConnStatus("CONNECTING");

        const ws = new WebSocket(url);

        ws.onopen = () => setConnStatus("CONNECTED");

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data && Array.isArray(data.services) && Array.isArray(data.alerts)) {
                    setSnapshot(data);
                }
            } catch {
                // ignore malformed messages
            }
        };

        ws.onerror = () => setConnStatus("ERROR");
        ws.onclose = () => setConnStatus("DISCONNECTED");

        return () => ws.close();
    }, [url]);

    return { snapshot, connStatus };
}