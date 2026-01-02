import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";

export function useTrendsVelocity() {
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        apiFetch<any[]>("/trends/velocity")
            .then(setData)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, []);

    return { data, loading };
}
