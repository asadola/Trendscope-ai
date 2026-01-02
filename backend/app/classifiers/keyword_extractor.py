import yake

_kw_extractor = yake.KeywordExtractor(lan="en", n=2, top=15, dedupLim=0.9)


def extract_keywords(text: str):
    keywords = _kw_extractor.extract_keywords(text)
    return [kw for kw, score in keywords]
