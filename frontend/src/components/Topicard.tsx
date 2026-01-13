import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getUnsplashImage } from "../utils/unsplash";
import { getTopicDescription } from "../utils/getTopicDescription";

export default function Topicard({
    topic,
    article_count,
    insight,
}: {
    topic: string;
    article_count: number;
    insight?: string;
}) {
    const navigate = useNavigate();
    const [image, setImage] = useState<string | null>(null);

    useEffect(() => {
        getUnsplashImage(topic).then(setImage);
    }, [topic]);

    return (
        <article
            onClick={() => navigate(`/topic/${topic}`)}
            className="group cursor-pointer bg-white rounded-3xl overflow-hidden shadow-soft hover:shadow-xl transition"
        >
            {/* IMAGE */}
            <div className="h-40 bg-slate-200">
                {image && (
                    <img
                        src={image}
                        alt={topic}
                        className="h-full w-full object-cover"
                    />
                )}
            </div>

            {/* CONTENT */}
            <div className="p-5 space-y-3">
                <span className="text-xs font-semibold text-red-600">
                    🔥 {article_count}+ articles
                </span>

                <h4 className="text-xl font-semibold capitalize group-hover:text-brand">
                    {topic}
                </h4>

                <p className="text-sm text-slate-600 line-clamp-2">
                    {getTopicDescription(
                        { topic, article_count, insight },
                        "trending"
                    )}
                </p>

                <span className="text-sm text-brand font-medium">
                    Read →
                </span>
            </div>
        </article>
    );
}
