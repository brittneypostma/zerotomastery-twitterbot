# This file will use the Tweepy Cursor API to reply to mentions, follow users that follow us, and a backup like and retweet

# Import tweepy, time, and the create_api function from config.py

import tweepy
from config import create_api
import time


# Define a check_mentions function that accepts api, keywords, and since_id, follow and reply to the user if user has mentioned us
# Define a follow_followers function that accepts api and check if they are not followed, then follow them
# Define a fav_retweet function that accepts api, create terms string to search for and use the tweepy.Cursor object to search those terms 100 times

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

            api.update_status(status="ZTMBot to the rescue!", in_reply_to_status_id=tweet.id)
    return new_since_id

# Define a main function to connect to the api and create a since_id counter, call all above functions
def main():
    since_id = 1
    while True:
        since_id = check_mentions(api, ["#ZTM", "#Zerotomastery"], since_id)
        time.sleep(60)
        
# if __name__ main, call the main function
if __name__ == "__main__":
    main()
