import os
import datetime as dt


class DataHandler(object):

    def __init__(self, social_network, search_words):

        self.search_words = search_words
        self.social_network = social_network

    def store_network_dataset(self, dataset):

        date = dt.datetime.now().strftime("%Y_%m_%d")
        directory_input = os.path.join(os.path.dirname(__file__), 'input')
        directory_log = os.path.join(os.path.dirname(__file__), 'log', 'input')

        #removes all files from the input directory
        for file in os.listdir(directory_input):

            filename = os.fsdecode(file)
            os.remove(os.path.join(directory_input, filename))

        #saves the new data in the input and input/log directory
        dataset.to_csv(os.path.join(directory_input, 'dataset.csv')
                       , sep=';', index=None)
        dataset.to_csv(os.path.join(directory_log
                       , self.social_network + self.search_words + date + '.csv')
                       , sep=';', index=None)

    def store_processed_dataset(dataset):
        pass