import configparser
import tweepy as tw

class Api(object):

    def __init__(self):
        pass

    @staticmethod
    def twitter_api():

        config = configparser.ConfigParser()
        config.read(r'api/configs.ini') 
        consumer_key = config['TWITTER']['consumer_key']
        consumer_secret = config['TWITTER']['consumer_secret']
        access_token = config['TWITTER']['access_token']
        access_token_secret = config['TWITTER']['access_token_secret']

        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        return tw.API(auth, wait_on_rate_limit=True)
