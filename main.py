import argparse
import nltk 
import spacy

import pandas as pd

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from spacy.lang.pt import Portuguese
from spacy.lang.pt.stop_words import STOP_WORDS

from pre_process.pre_processing import Processing
from social_collector.collect_data import CollectData


def get_args():

  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--search-words',
      '-sw',
      default = 'Política',
      type = str,
      help = 'topic that will be researched on twitter')
  parser.add_argument(
      '--social-network',
      '-sn',
      default = ['twitter'],
      nargs='+',
      help = 'social network that will be researched, can be more than one')
  parser.add_argument(
      '--n-tweets',
      '-nt',
      default = 200,
      type = int,
      help = 'number of tweets that will be collected from twitter')

  return parser.parse_args()


def main(search_words, n_tweets):

    nlp = spacy.load('pt')
    nltk.download("stopwords")
    nltk.download('punkt')
    stop_words = set(stopwords.words('portuguese'))
    nltk.download('rslp')
    
    df = Twitter.get_tweets(search_words, n_tweets) # DataFrame
    Processing.words_dataset(df['tweets'], stop_words, nlp)
    all_words, all_words_n_gram = Processing.words_dataset(df['tweets'], stop_words, nlp) # Get all dataset words
    pairs = Processing.words_frequency(all_words) # Words Frequency

    bag_of_words = []
    bag_of_words_n_gram = []
    clean_tweets = []
    # Cleaning tweets dataset
    count = 0
    for element in df['tweets']:

        if count < 10: # Testing just with the firts tweets
            x = Processing.clean(element)
            y = Processing.tokenize(x)
            z = Processing.nltk_stop_words(y, stop_words)
            k = Processing.spacy_stop_words(z, nlp)
            p = Processing.lemma(k, nlp)
            t, size = Processing.concatenate(p)
            w = Processing.n_gram(t, size)
            m = Processing.bag_of_words(w, all_words_n_gram)
            t = Processing.bag_of_words(p, all_words)
            bag_of_words_n_gram.append(m)
            bag_of_words.append(t)
            clean_tweets.append(t)
        count += 1

    df_clean = pd.DataFrame({"Tweets": clean_tweets, "Bag of words ": bag_of_words, "N-gram": bag_of_words_n_gram})

    return df_clean
    

if __name__ == "__main__":
    import pdb; pdb.set_trace()
    args = get_args()

    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)

    collector = CollectData(social_networks, search_words, n_tweets)
    collector.network_handler()
    
