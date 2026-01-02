from transformers import pipeline

_generator = pipeline(
    "text-generation",
    model="google/flan-t5-base",  # free + good explanations
    max_length=512,
)

def generate_insight(topic, articles):
    context = " ".join(a["content"][:800] for a in articles[:4])

    prompt = f"""
You are a senior news analyst.

Explain the topic: "{topic}" in simple, natural language.
Avoid buzzwords.
Be clear and informative.

Context:
{context}

Return:
1. Explanation
2. Why it matters
3. 3 key takeaways
"""

    output = _generator(prompt)[0]["generated_text"]

    return parse_output(output)
def parse_output(text):
    parts = text.split("\n")

    return {
        "explanation": parts[0],
        "why_it_matters": parts[1] if len(parts) > 1 else "",
        "key_points": [p for p in parts[2:5] if p],
    }
