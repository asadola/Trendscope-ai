import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";

export function useFeaturedInsights(limit = 5) {
    const [insights, setInsights] = useState<any[]>([]);

    useEffect(() => {
        apiFetch<any[]>(`/insights/ai?limit=${limit}`)
            .then(setInsights)
            .catch(() => { });
    }, [limit]);

    return insights;
}
