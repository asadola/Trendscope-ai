export function topicLabel(topic: string) {
    const map: Record<string, string> = {
        general: "General Coverage",
        ai: "Artificial Intelligence",
        politics: "Politics",
        health: "Health",
        technology: "Technology",
        weather: "Weather",
    };

    return map[topic] ?? topic;
}
