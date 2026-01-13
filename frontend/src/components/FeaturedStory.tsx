import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getUnsplashImage } from "../utils/unsplash";
import { COPY } from "../constants/editorialCopy";
import { getTopicDescription } from "../utils/getTopicDescription";




interface FeaturedStoryProps {
    topic: string;
    insight?: string;
}

export default function FeaturedStory({ topic, insight }: FeaturedStoryProps) {
    const navigate = useNavigate();
    const [image, setImage] = useState<string | null>(null);

    useEffect(() => {
        getUnsplashImage(topic).then(setImage);
    }, [topic]);

    return (
        <section
            onClick={() => navigate(`/topic/${topic}`)}
            className="cursor-pointer grid lg:grid-cols-2 gap-10 items-center"
        >
            {/* IMAGE */}
            <div className="relative h-72 rounded-3xl overflow-hidden bg-slate-200">
                {image && (
                    <img
                        src={image}
                        alt={topic}
                        className="h-full w-full object-cover"
                    />
                )}

                <div className="absolute inset-0 bg-black/40 flex items-end p-6">
                    <span className="text-white text-sm font-semibold uppercase tracking-widest">
                        Featured Story
                    </span>
                </div>
            </div>

            {/* CONTENT */}
            <div className="space-y-4">
                <h3 className="text-3xl font-extrabold capitalize leading-tight">
                    {topic}
                </h3>

                <p className="text-slate-600">
                    {getTopicDescription(
                        {
                            topic,
                            article_count: 999, // editorial weight
                            insight,
                        },
                        "featured"
                    )}
                </p>

                <span className="text-brand font-semibold">
                    Read full coverage →
                </span>
            </div>
        </section>
    );
}
