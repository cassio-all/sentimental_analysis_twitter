import nltk 
import spacy
import os
import re
import string, collections
import nltk, re, string, collections
import sklearn.feature_extraction.text as txt

import pandas as pd

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.util import ngrams
from spacy.lang.pt import Portuguese
from spacy.lang.pt.stop_words import STOP_WORDS

from social_collector.collect_data import CollectData

from unidecode import unidecode 


class Processing(object):

    def __init__(self, tweet):

        self.tweet

    # Function to clean text
    def clean(self, tweets):

        tweet = unidecode(tweet)
        tweet = tweet.replace('"', ' ')
        tweet = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", tweet)
        tweet = tweet.lower()

        return tweets

    # Function to tokenize 
    def tokenize(self, tweets):

        word_tokens = word_tokenize(tweet)

        return word_tokens

    # Function to remove nltk stopwords
    def nltk_stop_words(self, word_tokens, stop_words):

        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        return filtered_sentence

    # Function to remove spacy stopwords
    def spacy_stop_words(self, filtered_sentence, nlp):

        filtered_sentence_ = []
        for w in filtered_sentence:
            lexeme = nlp.vocab[w]
            if lexeme.is_stop == False:
                filtered_sentence_.append(w)

        return filtered_sentence_

    # Function to lemmas
    def lemma(self, filtered_sentence_, nlp):

        filtered_sentence_lemma = []
        for w in filtered_sentence_:
            doc = nlp(w)
            tokens = [tok for tok in doc]
            for token in tokens:
                if token.pos_ == 'VERB':
                    filtered_sentence_lemma.append(token.lemma_)
                else:
                    filtered_sentence_lemma.append(w)
                    
        return filtered_sentence_lemma

    # Function to concatenate words in a sentence
    def concatenate(self, filtered_sentence_lemma):

        size = 2
        if len(filtered_sentence_lemma) == 1:
            size = 1
        final_phrase = ""
        for word in filtered_sentence_lemma:
            final_phrase += word + " "

        return final_phrase, size


     # Function to apply n-gram (bi-grams? tri-grams?)
    def n_gram(self, sentence, size):

        sentence = [sentence]
        vect = txt.CountVectorizer(ngram_range=(size,size))
        txt.d
        vect.fit(sentence)
        ngram_words = vect.get_feature_names()

        return ngram_words

    # Function to create a bag
    def bag_of_words(self, words, all_words):

        bag = [0]*len(all_words)
        for s in words:
            for i,w in enumerate(all_words):
                if w == s:
                    bag[i] = 1
        return bag

    # All words in dataset
    def words_dataset(self, sentence, stop_words, nlp):
        
        all_words = []
        all_words_n_gram = []
        for element in sentence:
            x = self.clean(element)
            y = self.tokenize(x)
            z = self.nltk_stop_words(y, stop_words)
            k = self.spacy_stop_words(z, nlp)
            p = self.lemma(k, nlp)
            l, size = self.concatenate(p)
            k = self.n_gram(l, size)
            for element in k:
                all_words_n_gram.append(element)
            for element_ in p:
                all_words.append(element_)

        return all_words, all_words_n_gram

    # Check words frequency
    def words_frequency(self, all_words):

        wordfreq = [all_words.count(w) for w in all_words]
        pairs = list(zip(all_words, wordfreq))

        return pairs


    def pre_processing(self):

        nlp = spacy.load('pt')
        nltk.download("stopwords")
        nltk.download('punkt')
        stop_words = set(stopwords.words('portuguese'))
        nltk.download('rslp')

        all_words, all_words_n_gram = Processing.words_dataset(df['tweets'], stop_words, nlp) # Get all dataset words
        pairs = Processing.words_frequency(all_words) # Words Frequency

        bag_of_words = []
        bag_of_words_n_gram = []
        clean_tweets = []

        for element in tweet:

            cleaned = self.clean(element)
            tok = self.tokenize(cleaned)
            stop_nltk = self.nltk_stop_words(tok)
            stop_spacy = self.spacy_stop_words(stop_nltk, nlp)
            lem = self.lemma(stop_spacy, nlp)
            sentence, size = self.concatenate(lem)
            n_gr = self.n_gram(sentence, size)
            bag_n_gr = self.bag_of_words(n_gr, all_words_n_gram)
            bag_w = self.bag_of_words(lem, all_words)
            bag_of_words.append(bag_w)
            bag_of_words_n_gram .append(bag_n_gr)
            clean_tweets.append(sentence)

        return pd.DataFrame({"Tweets": clean_tweets, "Bag of words ": bag_of_words, "N-gram": bag_of_words_n_gram})

        




        












