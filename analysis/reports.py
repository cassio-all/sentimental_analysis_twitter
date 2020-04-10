import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data.data_handler import DataHandler
import os


class Analysis(object):

    def __init__(self, social_networks, search_word):
        
        self.social_network = social_networks
        self.search_word = search_word

    def reports(self):

        handler = DataHandler(self.social_network, self.search_word)
        df_network = handler.read_predicted_dataset()
        hash_ = df_network.hashtag.unique()
    
        fig, ax = plt.subplots()
        sns.despine(left=True)
        for i in range(len(hash_)):
            ax = sns.distplot(df_network[df_network['hashtag'] == hash_[i]]['sentiment'] ,kde=False,label=hash_[i])

        ax.set_xlabel('Hashs')
        ax.get_yaxis().set_visible(False)
        ax.legend()
        plt.show()

        directory_plot = os.path.join(os.path.dirname(__file__), 'plots')
        plt.savefig(os.path.join(directory_plot, 'hist.png'))

