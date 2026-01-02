from app.classifiers.topic_classifier import classify_topic

sample_text = """
Stock markets rallied today as investors reacted to
new inflation data and comments from the central bank
about interest rate cuts.
"""

result = classify_topic(sample_text)
print(result)
