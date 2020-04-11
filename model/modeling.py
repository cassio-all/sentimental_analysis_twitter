from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from data.data_handler import DataHandler
from pre_process.pre_processing import Processing
import pandas as pd

class ExtractSentiment(object):
    
    def __init__(self, social_networks, search_word):
        
        self.social_network = social_networks
        self.search_word = search_word

    def vader_sentiment(self):

        handler = DataHandler(self.social_network, self.search_word)
        df_network = handler.read_network_dataset()
        df = df_network[df_network.tweet != '']
        
        prepross = Processing(self.social_network, self.search_word)
        analyzer = SentimentIntensityAnalyzer()

        predict_df = pd.DataFrame(None, columns=['date', 'hashtag', 'tweet', 'clean_tweet', 'sentiment'])

        for i, row in df.iterrows():

            clean_tweet = prepross.clean_text(row['tweet'])
            sentiment = analyzer.polarity_scores(clean_tweet)['compound']
            predict_df.loc[i] = [row['created_at'], row['hashtag'], row['tweet'], clean_tweet, sentiment]

        predict_df.to_csv(r'data/output/dataset_predict.csv', sep=';', index=None) #
