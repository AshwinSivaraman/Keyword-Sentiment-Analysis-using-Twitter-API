import tweepy
import preprocessor as p
from textblob import TextBlob
import statistics
from typing import List

from secrets import consumer_key, consumer_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def get_tweets(keyword: str) -> List[str]:
    all_tweets = []
    for tweet in tweepy.Cursor(api.search, q=keyword, tweet_mode="extended", lang='en').items(10):
        all_tweets.append(tweet.full_text)

    return all_tweets


def clean_tweets(all_tweets: List[str]) -> List[str]:
    tweets_clean = []
    for tweet in all_tweets:
        tweets_clean.append(p.clean(tweet))

    return tweets_clean


def get_sentiment(tweets_clean: List[str]) -> List[float]:
    sentiment_scores = []
    for tweet in tweets_clean:
        blob = TextBlob(tweet)
        sentiment_scores.append(blob.sentiment.polarity)

    return sentiment_scores


def get_average_sentiment(keyword: str) -> int:
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_sentiment(tweets_clean)

    average_score = statistics.mean(sentiment_scores)

    return average_score


if __name__ == "__main__":

    print("what does the world prefer?\n")
    print("First input:")
    a = input()
    print("Second input:")
    b = input()

    a_score = get_average_sentiment(a)
    b_score = get_average_sentiment(b)

    if(a_score > b_score):
        print(f"Twitter users prefer {a} to {b}")
        print(f"Score of {a} is {a_score}")
        print(f"Score of {b} is {b_score}")

    if(b_score > a_score):
        print(f"Twitter users prefer {b} to {a}")
        print(f"Score of {b} is {b_score}")
        print(f"Score of {a} is {a_score}")
