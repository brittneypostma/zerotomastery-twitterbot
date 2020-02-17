from os import getenv

from environs import Env
import tweepy


env = Env()
env.read_env()



def create_api():
    """This function collects the consumer and access keys, creates an api object and returns the authenticated api
    object.

    :return: authenticated api object
    """
    consumer_key = env.str('CONSUMER_KEY')
    consumer_secret = env.str('CONSUMER_SECRET')
    access_token = env.str('ACCESS_TOKEN')
    access_token_secret = env.str('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    return authenticate_api(api)


def authenticate_api(api):
    """This function verifies the credentials and returns the authenticated api object

    :param api: api object
    :return: authenticated api object
    :raises TweepError: raised due to an error Twitter Responded with or raised when an API method fails due to hitting
    Twitter’s rate limit.
    """
    try:
        api.verify_credentials()
    except tweepy.TweepError as error:
        raise error
    print("API created")
    return api

