class TrendScorer:

    def score(self, keyword_count: int, source_count: int):
        return keyword_count * (1 + source_count * 0.1)
