# imports: tweepy and os


# Define a function create_api to use os.getenv to access our tokens

# Keys are called:
# CONSUMER_KEY
# CONSUMER_SECRET
# ACCESS_TOKEN
# ACCESS_TOKEN_SECRET

# Use tweep OAuth to connect to the tweepy API and include a try except block to verify credentials and catch errors,
# return api

from os import getenv

import tweepy


def create_api():
    """This function collects the consumer and access keys and returns authenticated api object.

    :return: authenticated api object
    :rtype: object
    """
    consumer_key = getenv('CONSUMER_KEY')
    consumer_secret = getenv('CONSUMER_SECRET')
    access_token = getenv('ACCESS_TOKEN')
    access_token_secret = getenv('ACCESS_TOKEN_SECRET')

    return authenticate_api(consumer_key, consumer_secret, access_token, access_token_secret)


def authenticate_api(consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str) -> object:
    """This function authenticates the consumer and access keys and returns an api object

    :param consumer_key:
    :type consumer_key: str
    :param consumer_secret:
    :type consumer_secret: str
    :param access_token:
    :type access_token: str
    :param access_token_secret:
    :type access_token_secret: str
    :return: tweepy api object
    :rtype: object
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
        return api
    except tweepy.TweepError as error:
        return error
