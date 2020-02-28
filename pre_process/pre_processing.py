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
    def clean(tweet):

        accent = unidecode(tweet)
        lw = accent.lower()
        asp = lw.replace('"', ' ')
        replaces = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", asp)
        digits_replace= ''.join([i for i in replaces if not i.isdigit()])

        return digits_replace

    @staticmethod
    def tokenize(replaces):

        token = word_tokenize(replaces)

        return token

    @staticmethod
    def stop_words_remove(word, stop_words):
        
        filtered_sentence = []
        for w in word:
            if w not in stop_words:
                filtered_sentence.append(w)

        return filtered_sentence

    @staticmethod
    def lemma(filtered_sentence_, nlp):

        filtered_sentence_lemma = []
        for w in filtered_sentence_:
            doc = nlp(w)
            for token in doc:
                if token.pos_ == 'VERB':
                    filtered_sentence_lemma.append(token.lemma_)
                else:
                    filtered_sentence_lemma.append(w)

        return filtered_sentence_lemma

    @staticmethod
    def concatenate(filtered_sentence_lemma):

        size = 2
        if len(filtered_sentence_lemma) == 1:
            size = 1
        final_phrase = ""
        for word in filtered_sentence_lemma:
            final_phrase += word + " "

        return final_phrase, size

    @staticmethod
    def word_cloud(posts):

        text = " ".join(review for review in posts)
        wordcloud = WordCloud(max_font_size=100,width = 1520, height = 535, background_color="white").generate(text)
        wordcloud.to_file("data/input/wordcloud.png")
      
    @staticmethod
    def n_gram(final_phrase, size):

        sentence = [final_phrase]

        if (sentence[0] == '') or (len(sentence[0]) < 3):
            return sentence[0]
            
        else:
            
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
    def words_dataset(sentence, stop_words, nlp):

        all_words = []
        all_words_n_gram = []
        for element in sentence:
            cleaned = Processing.clean(element)
            token = Processing.tokenize(cleaned)
            stop_w = Processing.stop_words_remove(token, stop_words)
            lemma_ = Processing.lemma(stop_w, nlp)
            concat, size = Processing.concatenate(lemma_)
            ngram_words = Processing.n_gram(concat, size)
            for element_ in ngram_words:
                all_words_n_gram.append(element_)
            for element_ in lemma_:
                all_words.append(element_)

        return all_words, all_words_n_gram

    @staticmethod
    def words_frequency(all_words):

        wordfreq = [all_words.count(w) for w in all_words]
        pairs = list(zip(all_words, wordfreq))

        return pairs


    def pre_processing(self):

        handler = DataHandler(self.social_network, self.search_word)
        df_network = handler.read_network_dataset()
        df = df_network[df_network.tweets != '']

        nlp = spacy.load('pt_core_news_sm')
        nltk.download("stopwords")
        nltk.download('punkt')

        STOP_WORDS.update({'vc', 'vcs', 'pq', 'ta', 'qq', 'vs', self.search_word}) # test
        stop_words_ = STOP_WORDS.union(stopwords.words('portuguese'))
        stop_words = [Processing.clean(stop) for stop in stop_words_]

        nltk.download('rslp')
        
        all_words, all_words_n_gram = Processing.words_dataset(df['tweets'], stop_words, nlp) # Get all dataset words

        bag_of_words = []
        bag_of_words_n_gram = []
        clean_tweets = []

        for element in df['tweets']:

            cleaned = Processing.clean(element)
            token = Processing.tokenize(cleaned)
            stop_w = Processing.stop_words_remove(token, stop_words)
            lemma_ = Processing.lemma(stop_w, nlp)
            concat, size = Processing.concatenate(lemma_)
            ngram_words = Processing.n_gram(concat, size)

            bag_ngram = Processing.bag_of_words(ngram_words, all_words_n_gram)
            bag_words = Processing.bag_of_words(lemma_, all_words)
            bag_of_words_n_gram.append(bag_ngram)
            bag_of_words.append(bag_words)

            clean_tweets.append(concat)


        Processing.word_cloud(clean_tweets)

        dataset = pd.DataFrame({"Posts": clean_tweets, "BOW": bag_of_words, "BOW-N": bag_of_words_n_gram})
        handler.store_processed_dataset(dataset)
