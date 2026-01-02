import trafilatura
from newspaper import Article
from langdetect import detect


def extract_article(url, html):
    data = trafilatura.extract(
        html, include_comments=False, include_tables=False, output_format="json"
    )

    if data:
        import json

        parsed = json.loads(data)
        return {
            "url": url,
            "title": parsed.get("title"),
            "content": parsed.get("text"),
            "published_at": parsed.get("date"),
            "language": parsed.get("language"),
        }

    # Fallback
    article = Article(url)
    article.download(input_html=html)
    article.parse()

    return {
        "url": url,
        "title": article.title,
        "content": article.text,
        "published_at": article.publish_date,
        "language": detect(article.text) if article.text else None,
    }
