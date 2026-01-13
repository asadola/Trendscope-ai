export interface VelocityTopic {
    topic: string;
    velocity: number;
    hotness: number;
    status: "breaking" | "trending" | "stable";
    article_count: number;
}

export interface AIInsight {
    topic: string;
    category: string;
    mentions: number;
    summary: string;
}

/** UI-ready topic */
export interface TrendTopic extends VelocityTopic {
    insight?: string;
    category?: string;
}
