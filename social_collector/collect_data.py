import configparser

import tweepy as tw
import pandas as pd

from api.api import Api
from data.data_handler import DataHandler


class CollectData(object):

    # search_words: Term for related tweets
    # social_networks: Social networks that will be collected the data
    # n_tweets: Number of Tweets

    def __init__(self, social_networks, search_words, n_tweets):

        self.search_words = search_words
        self.social_networks = social_networks
        self.n_tweets = n_tweets

    def network_handler(self):

        for social_network in self.social_networks:

            if social_network == 'twitter':
                self.get_tweets()

    def get_tweets(self):

        api = Api.twitter_api()
        tweets_ = []
        created = []
        hashtag = []

        for search_word in self.search_words:

            new_search = search_word + " -filter:retweets" # Filter retweets
            tweets = tw.Cursor(api.search , q=new_search, lang = 'en').items(self.n_tweets)

            for tweet in tweets:
                tweets_.append(tweet.text) # Get tweets
                created.append(tweet.created_at) # Get timestamp
                hashtag.append(search_word)

        dataset = pd.DataFrame({"hashtag": hashtag, "created_at": created, "tweet": tweets_})
        store_data = DataHandler('twitter', self.search_words)
        store_data.store_network_dataset(dataset)
