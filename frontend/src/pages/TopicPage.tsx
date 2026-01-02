import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";
import type { TopicDetailResponse } from "../types/topicDetail";

export default function TopicPage() {
    const { topic } = useParams<{ topic: string }>();

    const [data, setData] = useState<TopicDetailResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!topic) return;

        apiFetch<TopicDetailResponse>(`/topics/${topic}`)
            .then(setData)
            .catch(() => setError("Failed to load topic"));
    }, [topic]);

    if (error) {
        return <div className="p-6 text-red-600">{error}</div>;
    }

    if (!data) {
        return <div className="p-6">Loading…</div>;
    }

    return (
        <div className="p-6 space-y-8">

            <h1 className="text-2xl font-bold capitalize">
                {data.topic}
            </h1>

            {/* INSIGHT */}
            <section className="bg-white p-6 rounded-xl shadow">
                <h2 className="font-semibold mb-2">Why it matters</h2>
                <p>{data.insight.why_it_matters}</p>

                <h2 className="font-semibold mt-4 mb-2">Outlook</h2>
                <p>{data.insight.outlook ?? data.insight.summary}</p>

                {!data.insight.fresh && (
                    <p className="mt-3 text-sm text-gray-500">
                        ℹ️ Early signal — limited coverage so far
                    </p>
                )}
            </section>

            {/* ARTICLES */}
            <section>
                <h2 className="font-semibold mb-4">
                    Supporting Articles ({data.article_count})
                </h2>

                <div className="space-y-4">
                    {data.articles.map((a) => (
                        <div key={a.url} className="border-b pb-4">
                            <h3 className="font-medium">{a.title}</h3>
                            <p className="text-sm text-gray-500">{a.source}</p>

                            <a
                                href={a.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-indigo-600 text-sm font-medium"
                            >
                                Read full article →
                            </a>
                        </div>
                    ))}
                </div>
            </section>

        </div>
    );
}
