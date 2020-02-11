# This file is for the Streaming tweepy API
# import time, tweepy, and the create_api function from config.py

# Create a class that accepts the tweepy.StreamListener

# Define an __init__ function inside the class that accepts self and api parameters

# Define an on_status function inside the class that accepts self and tweet parameters, retweet and favorite if the tweet has not been already

# Define an on_error function inside the class to catch errors

################### END OF CLASS ########################

# Define a main function that takes keywords and ids and connects to the tweepy stream api using those keywords and ids to track and follow

# if __name__ main define keywords to search for and ids to follow and run the main function with those

import tweepy

from config import create_api

follow_list = ["224115510", "2998698451",
               "743086819"]  # The first is for Andrei Neagoie, The second for Yihua Zhang and the third for Daniel Bourke Yihua Zhang and the third for Daniel Bourke


class MyStreamListener(tweepy.StreamListener):
    """

    """

    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        if tweet.in_reply_to_status_id is not None or \
                tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except tweepy.TweepError as error:
                raise error
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
            except tweepy.TweepError as error:
                raise error

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False


api = create_api()

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
