# Social Network Sentimental analysis

Project whose the aim is to capture Social Network posts and extract the feeling from them. To this end, the program will collect data from social networks given some user choices (as a topic to search on Twitter), store, treat and model seeking to identify the feeling expressed in the post as positive or negative. Different sentiment analysis techniques will be tested to seek the best result.

## Getting Started/Requirements/Prerequisites/Dependencies

- run <strong>pip install -r requirements.txt</strong> to install the requirements in your environment
- visit [twitter-develop](https://developer.twitter.com/) and create a Twitter account if you don't have one. You'll need to generate access keys and add them to the file api/configs.ini
- Running:
    - the program so far has three  input variables, all of which are optional. They are: which social network wants to collect data, hashtag you want to search on Twitter, number of tweets you want to collect. The default is: <em>twitter</em>, <em>política</em>, <em>200</em>, respectively.

## TODO
- Create functions to pre-process the data
- Create the <em>method</em> input variable to allow the collection, pre-processing and modeling steps to be run separately
- Create sentiment analysis models and apply on a pre-processed data

## Authors

* **Cássio de Alcantara** - [cassio-all](https://github.com/cassio-all)
* **João Lucas Flauzino Cassiano** - [joaoflauzino](https://github.com/joaoflauzino)

See also the list of [contributors](https://github.com/cassio-all/sentimental_analysis_twitter/graphs/contributors) who participated in this project.