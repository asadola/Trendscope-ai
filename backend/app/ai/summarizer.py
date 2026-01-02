from transformers import pipeline

_summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=-1,  # CPU
)

def summarize_text(text, max_length=120):
    if len(text.split()) < 50:
        return text

    summary = _summarizer(
        text,
        max_length=max_length,
        min_length=40,
        do_sample=False,
    )

    return summary[0]["summary_text"]
