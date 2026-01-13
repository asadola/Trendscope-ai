import type { VelocityTopic } from "../types/trends";

type TopicLike = {
    topic: string;
    article_count: number;
    status?: string;
    insight?: string;
};

export function getTopicDescription(
    topic: TopicLike,
    mode: "featured" | "trending" | "quiet"
): string {

    // Insight ONLY if it exists (Topic page / featured)
    if (typeof topic.insight === "string" && topic.insight.length > 40) {
        return topic.insight;
    }

    // Section-based intelligence
    if (mode === "featured") {
        return "This topic is shaping the current news narrative and drawing strong editorial focus.";
    }

    if (mode === "trending") {
        return `Coverage is accelerating rapidly across multiple sources, with ${topic.article_count} related articles detected.`;
    }

    if (mode === "quiet") {
        return "Limited coverage so far, but early signals suggest emerging importance.";
    }

    return "This topic is being monitored by TrendScope AI.";
}
