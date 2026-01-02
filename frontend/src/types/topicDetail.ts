export interface TopicInsight {
    summary: string | null;
    why_it_matters: string | null;
    outlook?: string | null;

    confidence: number | null;
    generated_at: string | null;
    fresh: boolean;
}

export interface TopicArticle {
    title: string;
    source: string;
    url: string;
    published_at?: string;
}

export interface TopicDetailResponse {
    topic: string;
    article_count: number;
    insight: TopicInsight;
    articles: TopicArticle[];
}
