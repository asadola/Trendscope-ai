import { useState } from "react";
import { apiFetch } from "../api/client";

export default function SubscribeModal({ onClose }: { onClose: () => void }) {
    const [email, setEmail] = useState("");
    const [phone, setPhone] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function submit() {
        setLoading(true);
        setError(null);

        try {
            await apiFetch("/subscribe", {
                method: "POST",
                body: JSON.stringify({ email, phone: phone || null }),
            });
            onClose();
            alert("Subscribed successfully 🚀");
        } catch (e: any) {
            setError(e.message || "Subscription failed");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
            <div className="bg-white rounded-2xl p-6 w-full max-w-md space-y-4">
                <h3 className="text-xl font-bold">Subscribe to Trend Alerts</h3>

                <input
                    type="email"
                    placeholder="Email address"
                    className="w-full border rounded-lg px-4 py-2"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />

                <input
                    type="tel"
                    placeholder="Phone (optional)"
                    className="w-full border rounded-lg px-4 py-2"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                />

                {error && <p className="text-sm text-red-600">{error}</p>}

                <div className="flex justify-end gap-3">
                    <button onClick={onClose} className="text-slate-500">
                        Cancel
                    </button>
                    <button
                        onClick={submit}
                        disabled={loading}
                        className="bg-brand text-white px-4 py-2 rounded-lg"
                    >
                        {loading ? "Submitting..." : "Subscribe"}
                    </button>
                </div>
            </div>
        </div>
    );
}
