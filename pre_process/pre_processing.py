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
from spacy.lang.en.stop_words import STOP_WORDS

from unidecode import unidecode

class Processing(object):

    # search_words: Term for related tweets
    # social_networks: Social networks that will be collected the data

    def __init__(self, social_networks, search_word):

        self.social_network = social_networks
        self.search_word = search_word

    @staticmethod
    def clean_text(document):

        stop_words_ = STOP_WORDS.union(stopwords.words('english'))
        stop_words = [unidecode(stop).lower() for stop in stop_words_]
        # Split to translate
        tokens = document.split()
        # Concatenate
        document = ' '.join(tokens)
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
        wordcloud.to_file("data/output/wordcloud.png")
      
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