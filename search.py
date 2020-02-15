# This file will use the Tweepy Cursor API to reply to mentions, follow users that follow us, and a backup like and retweet
# imports tweepy, time, and the create_api function from config.py
from typing import List

import tweepy
import time
from config import create_api

# Define a follow_followers function that accepts api and check if they are not followed, then follow them
followed_users_ids: List[str] = []  # Todo: Is user id string or integer?


def follow_followers(api):
    """Follow all followers."""
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            follower.follow()
            followed_users_ids.append(follower.id)
            print('Followed ', follower.name)


def unfollow(api):
    """Unfollow if a followed user is no longer following."""
    for user_id in followed_users_ids: #check list for followers against api
        try:
            if not api.exists_friendship(source_screen_name='@KC_Kellebrities',
                                         target_id=user_id):
                api.destroy_friendship(id=user_id)
                time.sleep(10)
                followed_users_ids.remove(user_id)
                print("Unfollowed:", user_id)
        except tweepy.RateLimitError:
            print("Rate Limit Exceeded")
            time.sleep(900)


# Define a check_mentions function that accepts api, keywords, and since_id, follow and reply to the user if user has mentioned us
def check_mentions(api, keywords, since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items(100):
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(status="\"while(!( succeed = try_again() ) )\" \nZero To Mastery, ZTMBot to the rescue! \nhttps://zerotomastery.io/",
                              in_reply_to_status_id=tweet.id)
    return new_since_id


# Define a fav_retweet function that accepts api, create terms string to search for and use the tweepy.Cursor object to search those terms 100 times
def fav_retweet(api):
    '''
    This function search for tweets in the with a search criteria
    and automatic like the tweet if the tweet has not been liked and
    retweet the tweet if the tweet has not been retweeted
    '''
    search = ["#ZTM", "#Zerotomastery"]
    for tweet in tweepy.Cursor(api.search, search).items(100):
        try:
            if not tweet.favorite():
                tweet.favorite()
                print("I have liked the tweet")
            if not tweet.retweet():
                tweet.retweet()
                print('Retweeted the tweet')
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


# Define a main function to connect to the api and create a since_id counter, call all above functions
def main():
    api = create_api()
    since_id = 1
    keywords = ["#ZTM", "#Zerotomastery",
                "#ztm", "zerotomastery", "ZeroToMastery"]
    while True:
        since_id = check_mentions(api, keywords, since_id)
        # fav_retweet(api)
        time.sleep(60)


# if __name__ main, call the main function
if __name__ == "__main__":
    main()
# This file will use the Tweepy Cursor API to reply to mentions, follow users that follow us, and a backup like and retweet
# imports tweepy, time, and the create_api function from config.py
import tweepy
import time
from config import create_api

# Define a follow_followers function that accepts api and check if they are not followed, then follow them


# Define a check_mentions function that accepts api, keywords, and since_id, follow and reply to the user if user has mentioned us
def check_mentions(api, keywords, since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items(100):
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(status="\"while(!( succeed = try_again() ) )\" \nZero To Mastery, ZTMBot to the rescue! \nhttps://zerotomastery.io/",
                              in_reply_to_status_id=tweet.id)
    return new_since_id


# Define a fav_retweet function that accepts api, create terms string to search for and use the tweepy.Cursor object to search those terms 100 times
def fav_retweet(api):
    '''
    This function search for tweets in the with a search criteria
    and automatic like the tweet if the tweet has not been liked and
    retweet the tweet if the tweet has not been retweeted
    '''
    search = ["#ZTM", "#Zerotomastery"]
    for tweet in tweepy.Cursor(api.search, search).items(100):
        try:
            if not tweet.favorite():
                tweet.favorite()
                print("I have liked the tweet")
            if not tweet.retweet():
                tweet.retweet()
                print('Retweeted the tweet')
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


def follow_followers(api):
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            follower.follow()
            followed.append(follower.id)
            print('Followed ', follower.name)


def unfollow(api):
    for user in followed:
        try:
            if (api.exists_friendship(source_screen_name='@KC_Kellebrities', target_id=user) == False):
                api.destroy_friendship(id=user)
                time.sleep(10)
                followed.remove(user)
                print("Unfollowed:", user)
        except:
            print("Rate Limit Exceeded")
            time.sleep(900)


# Define a main function to connect to the api and create a since_id counter, call all above functions
def main():
    api = create_api()
    since_id = 1
    keywords = ["#ZTM", "#Zerotomastery",
                "#ztm", "zerotomastery", "ZeroToMastery"]
    while True:
        since_id = check_mentions(api, keywords, since_id)
        # fav_retweet(api)
        time.sleep(60)


# if __name__ main, call the main function
if __name__ == "__main__":
    main()
