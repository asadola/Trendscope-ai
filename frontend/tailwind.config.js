/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                brand: "#4F46E5",
            },
            boxShadow: {
                soft: "0 8px 24px rgba(0,0,0,0.06)",
            },
        },
    },
    plugins: [],

    extend: {
        colors: {
            brand: "#4F46E5",
            accent: "#F97316",
            success: "#22C55E",
        },
        boxShadow: {
            soft: "0 10px 30px rgba(0,0,0,0.08)",
        },
    }

};
