const UNSPLASH_KEY = import.meta.env.VITE_UNSPLASH_KEY as string;

export async function getUnsplashImage(topic: string): Promise<string | null> {
    try {
        const res = await fetch(
            `https://api.unsplash.com/search/photos?query=${encodeURIComponent(
                topic
            )}&orientation=landscape&per_page=1`,
            {
                headers: {
                    Authorization: `Client-ID ${UNSPLASH_KEY}`,
                },
            }
        );

        const data = await res.json();
        return data.results?.[0]?.urls?.regular ?? null;
    } catch (err) {
        console.error("Unsplash error:", err);
        return null;
    }
}
