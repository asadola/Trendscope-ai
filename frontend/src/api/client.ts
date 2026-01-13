const API_BASE = "http://127.0.0.1:8000/api";

export async function apiFetch<T>(
    path: string,
    options: RequestInit = {}
): Promise<T> {
    const res = await fetch(`${API_BASE}${path}`, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });

    if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Request failed");
    }

    return res.json();
}
