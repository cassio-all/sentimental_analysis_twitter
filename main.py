import argparse

import pandas as pd

from pre_process.pre_processing import Processing
from social_collector.collect_data import CollectData


def get_args():

  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--search-words',
      '-sw',
      default = 'Política',
      type = str,
      help = 'topic that will be researched on twitter')
  parser.add_argument(
      '--social-network',
      '-sn',
      default = ['twitter'],
      nargs='+',
      help = 'social network that will be researched, can be more than one')
  parser.add_argument(
      '--n-tweets',
      '-nt',
      default = 200,
      type = int,
      help = 'number of tweets that will be collected from twitter')

  return parser.parse_args()


if __name__ == "__main__":

    args = get_args()

    collector = CollectData(args.social_network, args.search_words, args.n_tweets)
    collector.network_handler()

    processing = Processing(args.social_network, args.search_words)
    processing.pre_processing()
