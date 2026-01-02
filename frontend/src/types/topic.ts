export type TopicStatus = "breaking" | "trending" | "stable";

export interface TopicVelocity {
    topic: string;
    velocity: number;
    hotness: number;
    status: TopicStatus;
    article_count: number;
}
