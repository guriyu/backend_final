from textblob import TextBlob

def get_sentiment_polarity(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    return polarity