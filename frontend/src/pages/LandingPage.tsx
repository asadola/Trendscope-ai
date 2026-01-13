import { useEffect, useState } from "react";
import { useTrendsVelocity } from "../hooks/useTrendsVelocity";
import { useSources } from "../hooks/useSources";
// import { useFeaturedInsights } from "../hooks/useFeaturedInsights";
import Topicard from "../components/Topicard";
import { useRef } from "react";
import { useNavigate } from "react-router-dom";
import { getTopicImage } from "../utils/topicImage";
import { getUnsplashImage } from "../utils/unsplash";
import FeaturedStory from "../components/FeaturedStory";
import { getTopicDescription } from "../utils/getTopicDescription";
import SubscribeModal from "../components/SubscribeModal";
import BreakingTicker from "../components/BreakingTicker";





export default function LandingPage() {
    const { data: topics, loading } = useTrendsVelocity();
    const sources = useSources();
    // const insights = useFeaturedInsights();
    const [query, setQuery] = useState("");
    const trendingRef = useRef<HTMLDivElement | null>(null);
    const navigate = useNavigate();
    const [showSubscribe, setShowSubscribe] = useState(false);
    const [breakingItems, setBreakingItems] = useState<any[]>([]);
    const [searchResults, setSearchResults] = useState<any[]>([]);






    const filteredTopics = topics.filter(t =>
        t.topic.toLowerCase().includes(query.toLowerCase())
    );

    const breaking = topics.filter(t => t.status === "breaking");
    const trending = [...topics]
        .sort((a, b) => b.article_count - a.article_count)
        .slice(0, 3);


    const fallbackTrending = trending.length
        ? trending
        : topics.slice(0, 6);


    const quietSignals = topics.filter(t =>
        t.article_count > 0 &&
        t.article_count < 150 &&     // low volume
        t.status !== "breaking"      // exclude breaking
    );


    const searchedTrending = query
        ? fallbackTrending.filter(t =>
            t.topic.toLowerCase().includes(query.toLowerCase())
        )
        : fallbackTrending;

    useEffect(() => {
        fetch("/api/trends/breaking")
            .then(res => res.json())
            .then(setBreakingItems)
            .catch(() => setBreakingItems([]));
    }, []);
    useEffect(() => {
        if (!query || query.length < 2) return;

        fetch(`/api/topics/search?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(setSearchResults)
            .catch(() => setSearchResults([]));
    }, [query]);




    return (
        <div className="min-h-screen bg-slate-50 text-slate-900">
            {showSubscribe && (
                <SubscribeModal onClose={() => setShowSubscribe(false)} />
            )}

            {/* ================= NAVBAR ================= */}
            <header className="sticky top-0 z-20 bg-white/90 backdrop-blur border-b">
                <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
                    <h1 className="font-bold text-xl">
                        TrendScope<span className="text-indigo-600">AI</span>
                    </h1>

                    <div className="relative w-full max-w-md">
                        <input
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Search topics…"
                            className="w-full"
                        />

                        {searchResults.length > 0 && (
                            <div className="absolute bg-white shadow rounded-lg mt-2 w-full z-50">
                                {searchResults.map(t => (
                                    <div
                                        key={t.topic}
                                        onClick={() => {
                                            navigate(`/topic/${t.topic}`);
                                            setSearchResults([]);
                                            setQuery("");
                                        }}
                                        className="px-4 py-2 hover:bg-slate-100 cursor-pointer"
                                    >
                                        <strong>{t.topic}</strong>
                                        <span className="text-xs text-slate-500 ml-2">
                                            {t.article_count} articles
                                        </span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>




                    <button
                        onClick={() => setShowSubscribe(true)}
                        className="bg-brand text-white px-4 py-2 rounded-lg hover:scale-105 transition"
                    >
                        Subscribe
                    </button>

                </div>
            </header>

            <main className="max-w-7xl mx-auto px-6 space-y-20 py-16">

                {/* ================= HERO ================= */}
                <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 text-white p-12">
                    <div className="max-w-2xl space-y-4">
                        <span className="uppercase text-xs tracking-widest text-white/80">
                            Live Intelligence
                        </span>

                        <h2 className="text-4xl font-extrabold leading-tight">
                            Real-time AI-Powered News Intelligence
                        </h2>

                        <p className="text-white/90">
                            Track breaking stories, emerging narratives, and quiet signals
                            before they become headlines.
                        </p>

                        <button
                            onClick={() => trendingRef.current?.scrollIntoView({ behavior: "smooth" })}
                            className="bg-white text-indigo-700 px-6 py-3 rounded-xl font-semibold hover:scale-105 transition"
                        >
                            Explore Trending →
                        </button>
                    </div>
                </section>

                {/* ================= BREAKING MARQUEE ================= */}
                {breakingItems.length > 0 && (
                    <section className="bg-gradient-to-r from-red-600 to-orange-500 text-white rounded-xl px-6 py-3 shadow-soft">
                        <div className="flex items-center gap-4 overflow-hidden">
                            <span className="font-bold uppercase tracking-wide shrink-0">
                                Breaking
                            </span>

                            <div className="whitespace-nowrap animate-marquee text-sm font-medium">
                                {breakingItems.map((item, i) => (
                                    <span
                                        key={i}
                                        onClick={async () => {
                                            const res = await fetch(`/api/topics/${item.topic}/top-article`);
                                            const data = await res.json();
                                            if (data?.url) window.open(data.url, "_blank");
                                        }}
                                        className="mx-8 cursor-pointer hover:underline"
                                    >
                                        <strong className="uppercase">
                                            {item.topic}
                                        </strong>
                                        {" — "}
                                        {item.summary}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </section>
                )}



                {/* ================= SOURCES ================= */}
                <section>
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-xl font-semibold">Explore Channels</h3>
                        <button className="text-brand text-sm font-medium hover:underline">
                            See all →
                        </button>
                    </div>

                    <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-6">
                        {Array.isArray(sources) &&
                            sources.map((s: any) => (
                                <button
                                    key={s.source}
                                    onClick={() => navigate(`/source/${encodeURIComponent(s.source)}`)}
                                    className="group bg-white rounded-xl shadow-soft p-4 flex flex-col items-center gap-2 hover:scale-105 transition"
                                >

                                    <div className="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold">
                                        {s.source[0]}
                                    </div>
                                    <span className="text-sm font-medium">{s.source}</span>
                                </button>

                            ))}
                    </div>

                </section>
                {trending[0] && (
                    <FeaturedStory
                        topic={trending[0].topic}
                        insight={trending[0].insight}
                    />
                )}


                <section ref={trendingRef}>
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-2xl font-bold">🔥 Trending Now</h3>
                        <span className="text-sm text-slate-500">
                            Live topics gaining momentum
                        </span>
                    </div>

                    {searchedTrending.length === 0 && !loading && (
                        <p className="text-slate-400">No trending topics right now.</p>
                    )}

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                        {!loading &&
                            searchedTrending.map(t => (
                                <Topicard
                                    key={t.topic}
                                    topic={t.topic}
                                    article_count={t.article_count}
                                    insight={t.insight}
                                />

                            ))}
                    </div>

                </section>


                <section>
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-bold">
                                {breakingItems.length === 0 ? "🟢 Emerging Signals" : "🟢 Quiet Signals"}
                            </h3>
                            <p className="text-sm text-slate-500">
                                {breakingItems.length === 0
                                    ? "No breaking stories right now — these are the next ones to watch."
                                    : "Low-volume topics with high future potential"}
                            </p>

                        </div>
                    </div>

                    <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
                        {quietSignals.map((t, i) => (
                            <div
                                key={t.topic}
                                onClick={() => navigate(`/topic/${t.topic}`)}
                                className="relative cursor-pointer rounded-3xl p-6 shadow-soft hover:shadow-xl transition overflow-hidden"
                            >
                                {/* subtle color strip */}
                                <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-emerald-400 to-cyan-400" />

                                <span className="text-xs uppercase tracking-widest text-slate-400">
                                    Quiet Signal
                                </span>

                                <h4 className="text-xl font-semibold capitalize mt-2 mb-3">
                                    {t.topic}
                                </h4>

                                <p className="text-sm text-slate-600">
                                    Limited coverage right now, but showing early patterns worth tracking.
                                </p>

                                <div className="mt-4 text-sm font-medium text-brand">
                                    Investigate →
                                </div>
                            </div>
                        ))}
                    </div>
                </section>





            </main>

            {/* ================= FOOTER ================= */}
            <footer className="border-t py-6 text-sm text-slate-500">
                <div className="max-w-7xl mx-auto px-6 flex justify-between">
                    <p>TrendScope AI — real-time topic intelligence</p>
                    <p>Data updated continuously</p>
                </div>
            </footer>


        </div>
    );
}

