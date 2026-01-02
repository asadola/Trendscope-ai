from urllib.parse import urlparse

def build_sources(articles):
    sources = []

    seen = set()
    for a in articles:
        domain = urlparse(a["url"]).netloc.replace("www.", "")
        if domain in seen:
            continue

        seen.add(domain)
        sources.append({
            "title": a["title"],
            "url": a["url"],
            "platform": domain.capitalize()
        })

        if len(sources) >= 5:
            break

    return sources
