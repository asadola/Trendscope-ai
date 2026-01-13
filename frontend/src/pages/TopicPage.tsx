import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";
import type { TopicDetailResponse } from "../types/topicDetail";


export default function TopicPage() {
    const { topic } = useParams<{ topic: string }>();
    const [data, setData] = useState<TopicDetailResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    const [articles, setArticles] = useState<any[]>([]);
    const [offset, setOffset] = useState(0);
    const [loadingMore, setLoadingMore] = useState(false);




    function deriveStatus(data: TopicDetailResponse) {
        if (!data.insight.fresh) return "early";
        if (data.article_count > 50) return "trending";
        return "active";
    }

    useEffect(() => {
        if (!topic) return;

        apiFetch<TopicDetailResponse>(`/topics/${topic}`)
            .then(setData)
            .catch(() => setError("Failed to load topic"));
    }, [topic]);

    useEffect(() => {
        if (!topic) return;

        apiFetch<any[]>(`/topics/${topic}/articles?limit=50&offset=0`)
            .then(setArticles)
            .catch(() => { });
    }, [topic]);

    async function loadMore() {
        if (!topic) return;

        setLoadingMore(true);
        const nextOffset = offset + 50;

        const more = await apiFetch<any[]>(
            `/topics/${topic}/articles?limit=50&offset=${nextOffset}`
        );

        setArticles(prev => [...prev, ...more]);
        setOffset(nextOffset);
        setLoadingMore(false);
    }

    if (error) {
        return <div className="p-6 text-red-600">{error}</div>;
    }

    if (!data) {
        return <div className="p-6">Loading…</div>;
    }

    const status = deriveStatus(data);

    const statusStyles: Record<string, string> = {
        early: "bg-yellow-50 text-yellow-700 border-yellow-200",
        trending: "bg-red-50 text-red-700 border-red-200",
        active: "bg-green-50 text-green-700 border-green-200",
    };
    let pastInserted = false;


    return (
        <div className="max-w-5xl mx-auto px-6 py-12 space-y-14">

            {/* ================= HEADER ================= */}
            <header className="space-y-4">
                <h1 className="text-4xl font-bold capitalize">
                    {data.topic}
                </h1>

                <div className="flex flex-wrap items-center gap-3 text-sm">
                    <span
                        className={`px-3 py-1 rounded-full border font-medium ${statusStyles[status]}`}
                    >
                        {status.toUpperCase()}
                    </span>

                    {!data.insight.fresh && (
                        <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-600 border">
                            Early signal
                        </span>
                    )}

                    <span className="text-slate-500">
                        {data.article_count} articles analysed
                    </span>
                </div>
            </header>

            {/* ================= AI INSIGHT ================= */}
            <section className="bg-white rounded-2xl shadow-soft p-8 space-y-6">
                <h2 className="text-2xl font-semibold flex items-center gap-2">
                    🤖 AI Insight
                </h2>

                <div>
                    <h3 className="font-semibold mb-1 text-slate-800">
                        Why it matters
                    </h3>
                    <p className="text-slate-700 leading-relaxed">
                        {data.insight.why_it_matters}
                    </p>
                </div>

                <div>
                    <h3 className="font-semibold mb-1 text-slate-800">
                        Outlook
                    </h3>
                    <p className="text-slate-700 leading-relaxed">
                        {data.insight.outlook ?? data.insight.summary}
                    </p>
                </div>
            </section>

            {/* ================= ARTICLES ================= */}
            <section>
                <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
                    📰 Supporting Coverage
                </h2>

                <div className="space-y-4">
                    {articles.map((a) => {
                        const articleCard = (
                            <article
                                key={a.url}
                                className="bg-white rounded-xl shadow-soft p-5 hover:shadow-lg transition"
                            >
                                <h3 className="font-medium text-slate-900 mb-2">
                                    {a.title}
                                </h3>

                                <div className="flex items-center justify-between text-sm">
                                    <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-600">
                                        {a.source}
                                    </span>

                                    <a
                                        href={a.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-brand font-medium hover:underline"
                                    >
                                        Read article →
                                    </a>
                                </div>
                            </article>
                        );

                        if (a.is_past && !pastInserted) {
                            pastInserted = true;
                            return (
                                <div key={a.url}>
                                    <div className="my-8 text-center text-slate-400 text-sm uppercase tracking-widest">
                                        Past coverage
                                    </div>
                                    {articleCard}
                                </div>
                            );
                        }

                        return articleCard;
                    })}

                </div>
                <div className="pt-6 text-center">
                    <button
                        onClick={loadMore}
                        disabled={loadingMore}
                        className="px-6 py-2 rounded-lg border bg-white hover:bg-slate-50 text-sm font-medium"
                    >
                        {loadingMore ? "Loading…" : "Read more"}
                    </button>
                </div>

            </section>

        </div>
    );
}
