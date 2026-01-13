import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";
import type { VelocityTopic, AIInsight, TrendTopic } from "../types/trends";

export function useTrendsVelocity() {
    const [data, setData] = useState<TrendTopic[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        Promise.all([
            apiFetch<VelocityTopic[]>("/trends/velocity"),
            apiFetch<AIInsight[]>("/insights/ai"),
        ])
            .then(([velocity, insights]) => {
                const insightMap = new Map<string, AIInsight>(
                    insights.map(i => [i.topic, i])
                );

                const merged: TrendTopic[] = velocity.map(v => ({
                    ...v,
                    insight: insightMap.get(v.topic)?.summary,
                    category: insightMap.get(v.topic)?.category,
                }));

                setData(merged);
            })
            .finally(() => setLoading(false));
    }, []);

    return { data, loading };
}
