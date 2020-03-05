import nltk 
import spacy
import os
import re
import string, collections
import nltk, re, string, collections
import sklearn.feature_extraction.text as txt

from data.data_handler import DataHandler

import pandas as pd

from wordcloud import WordCloud
import matplotlib.pyplot as plt

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.util import ngrams
from spacy.lang.pt.stop_words import STOP_WORDS

from unidecode import unidecode

class Processing(object):

    # search_words: Term for related tweets
    # social_networks: Social networks that will be collected the data

    def __init__(self, social_networks, search_word):

        self.social_network = social_networks
        self.search_word = search_word

    @staticmethod
    def clean_text(document, stop_words):

        # Remove accents
        document = unidecode(document)
        # Remove https, mentions, special characters, single character
        document = re.sub("(@[A-Za-z0-9]+)|(_[A-Za-z0-9]+)|(\w+:\/\/\S+)|(\W_)", " ", document).lower()
        # Remove pontuaction
        document = re.sub('['+string.punctuation+']', '', document)
        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)
        # Remove digits
        document = ''.join([i for i in document if not i.isdigit()])
        # Remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
        # Split
        tokens = document.split()
        # Stopwords
        tokens = [w for w in tokens if w not in stop_words]
        # Concatenate
        preprocessed_text = ' '.join(tokens)
    
        return preprocessed_text


    @staticmethod
    def lemma(tokens, nlp):
        # Lemmatization
        tokens = [(lem.lemma_ if lem.pos_ == 'VERB' else word)  for word in tokens for lem in nlp(word)]

        return tokens

    @staticmethod
    def word_cloud(posts):

        text = " ".join(review for review in posts)
        wordcloud = WordCloud(max_font_size=100,width = 1520, height = 535, background_color="white").generate(text)
        wordcloud.to_file("data/input/wordcloud.png")
      
    @staticmethod
    def n_gram(final_phrase):

        size = 2
        sentence = [final_phrase]
        if (sentence[0] == '') or (len(sentence[0]) < 3):
            return sentence[0]
        else:
            if len(sentence[0].split()) == 1:
                size = 1
            vect = txt.CountVectorizer(ngram_range=(size, size))
            vect.fit(sentence)
            ngram_words = vect.get_feature_names()

        return ngram_words

    @staticmethod
    def bag_of_words(words, all_words):

        bag = [0]*len(all_words)
        for s in words:
            for i,w in enumerate(all_words):
                if w == s:
                    bag[i] = 1
        return bag

    @staticmethod
    def words_dataset(sentences, stop_words, nlp):

        all_words = []
        all_words_n_gram = []

        for element in sentences:
            # Clean text
            sentence = Processing.clean_text(element, stop_words)
            # Lemma
            token = Processing.lemma(sentence.split(), nlp)
            sentence = ' '.join(token)
            # N Gram
            ngram_words = Processing.n_gram(sentence)
            for n in ngram_words:
                all_words_n_gram.append(n)
            # Tokenize
            tokens = sentence.split()
            # All dataset words dictionary
            for token in tokens:
                all_words.append(token)

        return all_words, all_words_n_gram


    def pre_processing(self):

        handler = DataHandler(self.social_network, self.search_word)
        df_network = handler.read_network_dataset()
        df = df_network[df_network.tweets != '']

        nlp = spacy.load('pt_core_news_sm')
        nltk.download("stopwords")
        nltk.download('punkt')

        STOP_WORDS.update({'vc', 'vcs', 'pq', 'ta', 'qq', self.search_word}) # test
        stop_words_ = STOP_WORDS.union(stopwords.words('portuguese'))
        stop_words = [unidecode(stop).lower() for stop in stop_words_]

        nltk.download('rslp')
        
        all_words, all_words_n_gram = Processing.words_dataset(df['tweets'], stop_words, nlp) # Get all dataset words

        bag_words = []
        bag_words_n_gram = []
        n_gram = []
        clean_tweets = []

        for sentence in df['tweets']:
            clean = Processing.clean_text(sentence, stop_words)
            token = Processing.lemma(clean.split(), nlp)
            concat = ' '.join(token)
            ngram = Processing.n_gram(concat)
            n_gram.append(Processing.n_gram(concat))
            bag_words_n_gram.append(Processing.bag_of_words(ngram, all_words_n_gram))
            bag_words.append(Processing.bag_of_words(concat.split(), all_words))
            clean_tweets.append(concat)

        Processing.word_cloud(clean_tweets)

        dataset = pd.DataFrame({"Posts": clean_tweets, "BOW": bag_words, "N-gram": n_gram, "BOW-N": bag_words_n_gram})
        handler.store_processed_dataset(dataset)
