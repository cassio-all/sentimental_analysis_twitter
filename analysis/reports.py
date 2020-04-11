import pandas as pd
from pandas.plotting import register_matplotlib_converters
from pandas.tseries import converter
import matplotlib.pyplot as plt
import seaborn as sns
from data.data_handler import DataHandler
import os

register_matplotlib_converters()

class Analysis(object):

    def __init__(self, social_networks, search_word):
        
        self.social_network = social_networks
        self.search_word = search_word

    def frequency(self, df_network):

        hash_ = df_network.hashtag.unique()
        fig, axs = plt.subplots(ncols = len(hash_), figsize=(10,10))

        count = 0
        for a in hash_:
            df_barchart = pd.DataFrame(df_network[df_network['hashtag'] == a]['sentiment_group'].value_counts()).reset_index().rename(columns={"index": "sentiment"})
            sns.set(style="whitegrid")
            sns.barplot(x="sentiment", y="sentiment_group", data=df_barchart, ax = axs[count]).set_title(a)
            count += 1

        del df_network

        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'plots')):
            os.mkdir(os.path.join(os.path.dirname(__file__), 'plots'))

        directory_plot = os.path.join(os.path.dirname(__file__), 'plots')
        plt.savefig(os.path.join(directory_plot, 'frequency.png'))


    def hist(self, df_network):

        hash_ = df_network.hashtag.unique()
        ax = plt.subplots(figsize=(10,10))
        sns.despine(left=True)
        for i in range(len(hash_)):
            ax = sns.distplot(df_network[df_network['hashtag'] == hash_[i]]['sentiment'] ,kde=False,label=hash_[i])

        ax.set_xlabel('Sentiment')
        ax.get_yaxis().set_visible(False)
        ax.legend()

        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'plots')):
                os.mkdir(os.path.join(os.path.dirname(__file__), 'plots'))

        directory_plot = os.path.join(os.path.dirname(__file__), 'plots')
        plt.savefig(os.path.join(directory_plot, 'hist.png'))

        del df_network


    def line(self, df_network):


        hash_ = df_network.hashtag.unique()
        date = 'date_day'
    
        df_network['date_day'] = pd.to_datetime(df_network['date']).dt.floor('d')
        if max(df_network['date_day']) == min(df_network['date_day']):
            df_network['date_hour'] = pd.to_datetime(df_network['date']).dt.floor('H')
            if max(df_network['date_hour'].dt.hour) == min(df_network['date_hour'].dt.hour):
                df_network['date_minute'] = pd.to_datetime(df_network['date']).dt.minute.astype(int)
                date = 'date_minute'
            else:
                date = 'date_hour'

        fig, axs = plt.subplots(ncols = len(hash_),  figsize=(10,10))
        sns.despine(left=True)

        count = 0
        for a in hash_:

            title = a + 'Sentiment Trend Over Time'
            df_pivot = pd.DataFrame(pd.pivot_table(df_network[df_network['hashtag'] == a][[date, 'sentiment_group']], columns=['sentiment_group'], values=['sentiment_group'], index=[date], aggfunc=len))
            df_pivot.reset_index(inplace = True)
            df_line = df_pivot.melt(date, var_name='class',  value_name='counts')
        
            if date == 'date_hour':
                title = a + ' - ' + 'por hora.'
            if date == 'date_minute':
                title = a + ' - ' + 'por minuto.'

            sns.lineplot(x=date, y="counts", hue='class', data=df_line, ax = axs[count]).set_title(title)
            count += 1

        del df_pivot, df_network

        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'plots')):
                os.mkdir(os.path.join(os.path.dirname(__file__), 'plots'))

        directory_plot = os.path.join(os.path.dirname(__file__), 'plots')
        plt.savefig(os.path.join(directory_plot, 'line.png'))


    def reports(self):

        handler = DataHandler(self.social_network, self.search_word)
        df_network = handler.read_predicted_dataset()
        df_network['sentiment_group'] = ["positive" if x >= 0.3 else ('negative' if x <= -0.3 else "neutral") for x in df_network['sentiment']]
        self.hist(df_network) # Creating histogram chart
        self.frequency(df_network) # Creating a bar chart
        #self.line(df_network) # Creating line chart



