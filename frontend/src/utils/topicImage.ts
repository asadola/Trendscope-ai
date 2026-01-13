export function getTopicImage(topic: string) {
    const t = topic.toLowerCase();

    if (t.includes("politic")) return "https://images.unsplash.com/featured/?politics";
    if (t.includes("ai")) return "https://images.unsplash.com/featured/?artificial-intelligence";
    if (t.includes("tech")) return "https://images.unsplash.com/featured/?technology";
    if (t.includes("health")) return "https://images.unsplash.com/featured/?health";
    if (t.includes("weather")) return "https://images.unsplash.com/featured/?weather";
    if (t.includes("finance")) return "https://images.unsplash.com/featured/?finance";

    // fallback
    return "https://images.unsplash.com/featured/?news";
}
