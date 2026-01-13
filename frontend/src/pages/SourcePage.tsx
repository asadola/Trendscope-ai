import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";

export default function SourcePage() {
    const { source } = useParams<{ source: string }>();
    const [articles, setArticles] = useState<any[]>([]);

    useEffect(() => {
        if (!source) return;

        apiFetch<any[]>(`/sources/${source}`)
            .then(setArticles)
            .catch(() => setArticles([]));

    }, [source]);

    return (
        <div className="max-w-5xl mx-auto px-6 py-12 space-y-8">
            <h1 className="text-3xl font-bold">{source}</h1>

            {articles.length === 0 && (
                <p className="text-slate-500">
                    No recent articles from this source yet.
                </p>
            )}

            <div className="space-y-4">
                {articles.map(a => (
                    <article
                        key={a.url}
                        className="bg-white p-5 rounded-xl border hover:shadow transition"
                    >
                        <h3 className="font-medium">{a.title}</h3>
                        <a
                            href={a.url}
                            target="_blank"
                            className="text-brand text-sm"
                        >
                            Read →
                        </a>
                    </article>
                ))}
            </div>
        </div>
    );
}
