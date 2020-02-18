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
from unidecode import unidecode 


class Processing(object):

    # Function to clean text
    def clean(tweet):

        tweet = unidecode(tweet)
        tweet = tweet.replace('"', ' ')
        tweet = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", tweet)
        tweet = tweet.lower()

        return tweet

    # Function to tokenize 
    def tokenize(tweet):

        word_tokens = word_tokenize(tweet)

        return word_tokens

    # Function to remove nltk stopwords
    def nltk_stop_words(word_tokens, stop_words):

        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        return filtered_sentence

    # Function to remove spacy stopwords
    def spacy_stop_words(filtered_sentence, nlp):

        filtered_sentence_ = []
        for w in filtered_sentence:
            lexeme = nlp.vocab[w]
            if lexeme.is_stop == False:
                filtered_sentence_.append(w)

        return filtered_sentence_

    # Function to lemmas
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

    # Function to concatenate words in a sentence
    def concatenate(filtered_sentence_lemma):

        size = 2
        if len(filtered_sentence_lemma) == 1:
            size = 1
        final_phrase = ""
        for word in filtered_sentence_lemma:
            final_phrase += word + " "

        return final_phrase, size


     # Function to apply n-gram (bi-grams? tri-grams?)
    def n_gram(sentence, size):

        sentence = [sentence]
        vect = txt.CountVectorizer(ngram_range=(size,size))
        txt.d
        vect.fit(sentence)
        ngram_words = vect.get_feature_names()

        return ngram_words

    # Function to create a bag
    def bag_of_words(words, all_words):

        bag = [0]*len(all_words)
        for s in words:
            for i,w in enumerate(all_words):
                if w == s:
                    bag[i] = 1
        return bag

    # All words in dataset
    def words_dataset(sentence, stop_words, nlp):
        
        all_words = []
        all_words_n_gram = []
        for element in sentence:
            x = Processing.clean(element)
            y = Processing.tokenize(x)
            z = Processing.nltk_stop_words(y, stop_words)
            k = Processing.spacy_stop_words(z, nlp)
            p = Processing.lemma(k, nlp)
            l, size = Processing.concatenate(p)
            k = Processing.n_gram(l, size)
            for element in k:
                all_words_n_gram.append(element)
            for element_ in p:
                all_words.append(element_)

        return all_words, all_words_n_gram

    # Check words frequency
    def words_frequency(all_words):

        wordfreq = [all_words.count(w) for w in all_words]
        pairs = list(zip(all_words, wordfreq))

        return pairs
        












