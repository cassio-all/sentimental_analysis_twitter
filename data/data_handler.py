import os
import datetime as dt
import pandas as pd


class DataHandler(object):

    def __init__(self, social_network, search_words): #

        self.search_words = search_words
        self.social_network = social_network

    def store_network_dataset(self, dataset):

        date = dt.datetime.now().strftime("%Y_%m_%d")
        directory_input = os.path.join(os.path.dirname(__file__), 'input')
        directory_log = os.path.join(os.path.dirname(__file__), 'log', 'input')

        #removes all network files from the input directory
        for file in os.listdir(directory_input):
            filename = os.fsdecode(file)
            if filename == 'dataset.csv':
                os.remove(os.path.join(directory_input, filename))

        search_words = ''
        for search_word in self.search_words:
            search_words += str(search_word)

        #saves the new data in the input and input/log directory
        dataset.to_csv(os.path.join(directory_input, 'dataset.csv')
                       , sep=';', index=None)
        dataset.to_csv(os.path.join(directory_log
                       , self.social_network + search_words + date + '.csv')
                       , sep=';', index=None)

    def store_processed_dataset(self, dataset):

        directory_input = os.path.join(os.path.dirname(__file__), 'input')
        
        #removes all processed files from the input directory
        for file in os.listdir(directory_input):
            filename = os.fsdecode(file)
            if filename == 'dataset_processed.csv':
                os.remove(os.path.join(directory_input, filename))

        #saves the new data in the input and input directory
        dataset.to_csv(os.path.join(directory_input, 'dataset_processed.csv'),
                       sep=';', index=None)

    def read_network_dataset(self):

        directory_input = os.path.join(os.path.dirname(__file__), 'input')

        return pd.read_csv(os.path.join(directory_input, 'dataset.csv'), sep =';')

    def read_processed_dataset(self):

        directory_input = os.path.join(os.path.dirname(__file__), 'input')

        return pd.read_csv(os.path.join(directory_input, 'dataset_processed.csv'), sep =';')

    def read_predicted_dataset(self):

        directory_input = os.path.join(os.path.dirname(__file__), 'output')

        return pd.read_csv(os.path.join(directory_input, 'dataset_predict.csv'), sep =';')
