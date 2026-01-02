import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";

export function useSources() {
    const [sources, setSources] = useState<Record<string, number>>({});

    useEffect(() => {
        apiFetch<Record<string, number>>("/trends/sources")
            .then(setSources)
            .catch(console.error);
    }, []);

    return sources;
}
