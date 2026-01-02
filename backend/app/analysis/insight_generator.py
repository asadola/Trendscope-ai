class InsightGenerator:
    """
    Converts trends and topics into human-readable insights.
    """

    def generate(self, topic: str, frequency: int, sources: list):
        top_sources = ", ".join([s["source"] for s in sources[:3]])

        return {
            "topic": topic,
            "summary": (
                f"The topic '{topic}' is currently trending with "
                f"{frequency} recent mentions. Coverage is being driven "
                f"primarily by {top_sources}."
            ),
            "confidence": "high" if frequency > 50 else "medium",
        }
