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
    """This function collects the consumer and access keys, creates an api object and returns the authenticated api
    object.

    :return: authenticated api object
    """
    consumer_key = getenv('CONSUMER_KEY')
    consumer_secret = getenv('CONSUMER_SECRET')
    access_token = getenv('ACCESS_TOKEN')
    access_token_secret = getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    return authenticate_api(api)


def authenticate_api(api):
    """This function verifies the credentials and returns the authenticated api object

    :param api: api object
    :return: authenticated api object
    """
    try:
        api.verify_credentials()
        print("Authentication OK")
        return api
    except tweepy.TweepError as error:
        return error
