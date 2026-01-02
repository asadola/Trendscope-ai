import { useNavigate } from "react-router-dom";
import type { TopicVelocity } from "../types/topic";

type Props = {
    data: TopicVelocity;
};

export default function TopicCard(props: Props) {
    const { data } = props;
    const navigate = useNavigate();

    const hotnessColor =
        data.hotness >= 2 ? "text-red-600" :
            data.hotness >= 1 ? "text-orange-500" :
                "text-slate-400";


    const color =
        data.status === "breaking"
            ? "border-red-500"
            : data.status === "trending"
                ? "border-yellow-500"
                : "border-gray-300";

    return (
        <div
            onClick={() => navigate(`/topic/${data.topic}`)}
            className={`card p-4 border-l-4 ${color}
    cursor-pointer
    transition-all duration-200
    hover:-translate-y-1 hover:shadow-lg`}
        >

            <h3 className="font-semibold text-lg capitalize">
                {data.topic}
            </h3>

            <p className="muted mt-1">
                {data.article_count} articles
            </p>
            <div className="mt-3 flex items-center justify-between text-sm">
                <span className="muted">{data.article_count} articles</span>

                <span className={`font-semibold ${hotnessColor}`}>
                    🔥 {data.hotness.toFixed(2)}
                </span>
            </div>


            <div className="mt-3 flex items-center justify-between text-sm">
                <span className="font-medium text-slate-700">
                    Velocity
                </span>
                <span className="text-brand font-semibold">
                    ⚡ {data.velocity.toFixed(2)}
                </span>
                <span className={`text-xs px-2 py-1 rounded-full
  ${data.status === "breaking" ? "bg-red-100 text-red-700" :
                        data.status === "trending" ? "bg-orange-100 text-orange-700" :
                            "bg-slate-100 text-slate-600"}`}>
                    {data.status.toUpperCase()}
                </span>

            </div>
        </div>
    );
}
