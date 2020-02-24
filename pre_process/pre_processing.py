import nltk 
import spacy
import os
import re
import string, collections
import nltk, re, string, collections
import sklearn.feature_extraction.text as txt

from data.data_handler import DataHandler

import pandas as pd

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.util import ngrams
from spacy.lang.pt import Portuguese
from spacy.lang.pt.stop_words import STOP_WORDS

from unidecode import unidecode

class Processing(object):

    def __init__(self, social_networks, search_word):

        self.social_network = social_networks
        self.search_words = search_word

    def clean(tweet):

        accent = unidecode(tweet)
        asp = accent.replace('"', ' ')
        replaces = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", asp)

        return replaces

    def tokenize(replaces):

        token = word_tokenize(replaces)

        return token

    def nltk_stop_words(word_tokens, stop_words):

        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        
        return filtered_sentence

    def spacy_stop_words(filtered_sentence, nlp):

        filtered_sentence_ = []
        for w in filtered_sentence:
            lexeme = nlp.vocab[w]
            if lexeme.is_stop == False:
                filtered_sentence_.append(w)

        return filtered_sentence_ 

    def lemma(filtered_sentence_, nlp):

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

    def concatenate(filtered_sentence_lemma):

        size = 2
        if len(filtered_sentence_lemma) == 1:
            size = 1
        final_phrase = ""
        for word in filtered_sentence_lemma:
            final_phrase += word + " "

        return final_phrase, size

    def n_gram(final_phrase, size):

        sentence = [final_phrase]

        if sentence[0] == '':
            return sentence[0]
            
        else:
            vect = txt.CountVectorizer(ngram_range=(size, size))
            vect.fit(sentence)
            ngram_words = vect.get_feature_names()

            return ngram_words

    def bag_of_words(words, all_words):

        bag = [0]*len(all_words)
        for s in words:
            for i,w in enumerate(all_words):
                if w == s:
                    bag[i] = 1
        return bag

    def words_dataset(sentence, stop_words, nlp):
        
        all_words = []
        all_words_n_gram = []
        for element in sentence:
            cleaned = Processing.clean(element)
            token = Processing.tokenize(cleaned)
            nltk_stop_sent = Processing.nltk_stop_words(token, stop_words)
            spacy_stop_sent = Processing.spacy_stop_words(nltk_stop_sent, nlp)
            lemma_ = Processing.lemma(spacy_stop_sent, nlp)
            concat, size = Processing.concatenate(lemma_)
            ngram_words = Processing.n_gram(concat, size)
            for element_ in ngram_words:
                all_words_n_gram.append(element_)
            for element_ in lemma_:
                all_words.append(element_)

        return all_words, all_words_n_gram

    def words_frequency(all_words):

        wordfreq = [all_words.count(w) for w in all_words]
        pairs = list(zip(all_words, wordfreq))
        
        return pairs


    def pre_processing(self):

        handler = DataHandler(self.social_network, self.search_words)
        df_network = handler.read_network_dataset()
        df = df_network[df_network.tweets != '']

        nlp = spacy.load('pt')
        nltk.download("stopwords")
        nltk.download('punkt')
        stop_words = set(stopwords.words('portuguese'))
        nltk.download('rslp')

        all_words, all_words_n_gram = Processing.words_dataset(df['tweets'], stop_words, nlp) # Get all dataset words
        #freq_words = Processing.words_frequency(all_words) # Words Frequency
        
        bag_of_words = []
        bag_of_words_n_gram = []
        clean_tweets = []

        for element in df['tweets']:

        
            cleaned = Processing.clean(element)
            token = Processing.tokenize(cleaned)
            nltk_stop_sent = Processing.nltk_stop_words(token, stop_words)
            spacy_stop_sent = Processing.spacy_stop_words(nltk_stop_sent, nlp)
            lemma_ = Processing.lemma(spacy_stop_sent, nlp)
            concat, size = Processing.concatenate(lemma_)
            ngram_words = Processing.n_gram(concat, size)

            bag_ngram = Processing.bag_of_words(ngram_words, all_words_n_gram)
            bag_words = Processing.bag_of_words(lemma_, all_words)
            bag_of_words_n_gram.append(bag_ngram)
            bag_of_words.append(bag_words)
        
            
            clean_tweets.append(concat)

        dataset = pd.DataFrame({"Posts": clean_tweets, "BOW": bag_of_words, "BOW-N": bag_of_words_n_gram})
        handler.store_processed_dataset(dataset)
