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


# if __name__ == "__main__":
#     create_api()
