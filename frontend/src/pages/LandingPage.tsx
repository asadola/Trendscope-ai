import { useState } from "react";
import { useTrendsVelocity } from "../hooks/useTrendsVelocity";
import { useSources } from "../hooks/useSources";
import { useFeaturedInsights } from "../hooks/useFeaturedInsights";
import TopicCard from "../components/Topicard";

export default function LandingPage() {
    const { data: topics, loading } = useTrendsVelocity();
    const sources = useSources();
    const insights = useFeaturedInsights();

    const [query, setQuery] = useState("");

    /* ----------------------------
       Filtering & segmentation
    ----------------------------- */

    const filteredTopics = topics.filter(t =>
        t.topic.toLowerCase().includes(query.toLowerCase())
    );

    const breaking = filteredTopics.filter(t => t.status === "breaking");
    const trending = filteredTopics.filter(t => t.status === "trending");
    const stable = filteredTopics.filter(t => t.status === "stable");

    return (
        <div className="px-6 max-w-7xl mx-auto space-y-16">

            {/* ================= HEADER ================= */}
            <header className="sticky top-0 z-10 bg-white border-b py-4 flex items-center justify-between gap-4">
                <h1 className="font-bold text-xl">TrendScope AI</h1>

                <input
                    type="text"
                    placeholder="Search topics…"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="border rounded-lg px-3 py-2 text-sm w-64"
                />

                <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg">
                    Subscribe
                </button>
            </header>

            {/* ================= BREAKING ALERT ================= */}
            {breaking.length > 0 && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4">
                    <p className="text-sm font-semibold text-red-700">
                        🚨 Breaking topics detected
                    </p>
                    <p className="text-sm text-red-600">
                        {breaking.map(t => t.topic).join(", ")}
                    </p>
                </div>
            )}

            {/* ================= EXPLORE CHANNELS ================= */}
            <section>
                <h2 className="section-title mb-1">Explore Channels</h2>
                <p className="muted mb-4">Sources contributing to today’s trends</p>

                <div className="flex gap-3 overflow-x-auto">
                    {Object.keys(sources).map(src => (
                        <div
                            key={src}
                            className="bg-white px-4 py-2 rounded-lg shadow text-sm whitespace-nowrap"
                        >
                            {src}
                        </div>
                    ))}
                </div>
            </section>

            {/* ================= BREAKING TOPICS ================= */}
            {breaking.length > 0 && (
                <section>
                    <h2 className="text-lg font-semibold text-red-600 mb-4">
                        Breaking Now
                    </h2>
                    <div className="flex gap-4 overflow-x-auto">
                        {breaking.map(t => (
                            <TopicCard key={t.topic} data={t} />
                        ))}
                    </div>
                </section>
            )}

            {/* ================= TRENDING TOPICS ================= */}
            <section>
                <h2 className="text-lg font-semibold mb-2">Trending Topics</h2>
                <p className="muted mb-4">Topics gaining momentum right now</p>

                {!loading && trending.length === 0 && (
                    <p className="muted">No trending topics yet.</p>
                )}

                <div className="grid md:grid-cols-3 gap-4">
                    {loading
                        ? <p className="muted">Loading…</p>
                        : trending.map(t => (
                            <TopicCard key={t.topic} data={t} />
                        ))}
                </div>
            </section>

            {/* ================= STABLE TOPICS ================= */}
            <section>
                <h2 className="section-title mb-2">Stable Topics</h2>
                <p className="muted mb-4">
                    Low activity — monitor for changes
                </p>

                <ul className="space-y-2">
                    {stable.map(t => (
                        <li
                            key={t.topic}
                            className="flex justify-between bg-white rounded-lg px-4 py-2 border"
                        >
                            <span className="capitalize">{t.topic}</span>
                            <span className="muted">{t.article_count}</span>
                        </li>
                    ))}
                </ul>
            </section>

            {/* ================= AI INSIGHTS ================= */}
            {insights.length > 0 && (
                <section>
                    <h2 className="text-lg font-semibold mb-4">AI Insights</h2>

                    <div className="grid md:grid-cols-2 gap-6">
                        {insights.map(i => (
                            <div
                                key={i.topic}
                                className="bg-white p-6 rounded-xl shadow"
                            >
                                <h3 className="font-semibold mb-2">{i.topic}</h3>
                                <p className="text-sm text-gray-600">{i.summary}</p>
                            </div>
                        ))}
                    </div>
                </section>
            )}

            {/* ================= FOOTER ================= */}
            <footer className="mt-24 border-t pt-8 text-sm text-slate-500">
                <div className="flex justify-between">
                    <p>TrendScope AI — real-time topic intelligence</p>
                    <p>Data updated continuously</p>
                </div>
            </footer>

        </div>
    );
}
