import { useEffect, useState } from "react";

interface BreakingItem {
    topic: string;
    summary: string;
    article_count: number;
}

export default function BreakingTicker() {
    const [items, setItems] = useState<BreakingItem[]>([]);

    useEffect(() => {
        fetch("/api/trends/breaking")
            .then(res => res.json())
            .then(setItems)
            .catch(() => setItems([]));
    }, []);

    if (!items.length) return null;

    return (
        <div className="bg-red-500 text-white py-2 overflow-hidden">
            <div className="animate-marquee whitespace-nowrap flex gap-10 px-6">
                {items.map((item, i) => (
                    <span key={i} className="font-semibold">
                        🔴 {item.topic.toUpperCase()}: {item.summary}
                    </span>
                ))}
            </div>
        </div>
    );
}
