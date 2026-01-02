from app.ai.summarizer import summarize_text

def summarize_by_category(articles):
    grouped = {}

    for a in articles:
        cat = a.get("category")
        if not cat:
            continue
        grouped.setdefault(cat, []).append(a["content"])

    summaries = {}
    for cat, contents in grouped.items():
        combined = " ".join(contents[:5])  # limit CPU
        summaries[cat] = summarize_text(combined)

    return summaries
