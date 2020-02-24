# This file will use the Tweepy Cursor API to reply to mentions, follow users that follow us, and a backup like and retweet
# imports tweepy, time, and the create_api function from config.py
from typing import List

import tweepy
import time
from config import create_api


# Define a follow_followers function that accepts api and check if they are not followed, then follow them
# Todo: Is user id string or integer? Use set
followed_users_ids: List[str] = []


def follow_followers(api):
    """Follow all followers."""
    for follower in tweepy.Cursor(api.followers).items():
        try:
            if not follower.following:
                follower.follow()
                followed_users_ids.append(follower.id)
                print('Followed ', follower.name)
                time.sleep(10)
        except tweepy.RateLimitError:
            print("Rate Limit Exceeded")
            time.sleep(900)


# Todo: Rename to unfollow_non_followers?
# def unfollow(api):
#     """Unfollow if a followed user is no longer following."""
#     for user_id in followed_users_ids:
#         try:
#             if not api.exists_friendship(source_screen_name='@ZtmBot',
#                                          target_id=user_id):
#                 api.destroy_friendship(id=user_id)
#                 time.sleep(10)
#                 followed_users_ids.remove(user_id)
#                 print("Unfollowed:", user_id)
#         except tweepy.RateLimitError:
#             print("Rate Limit Exceeded")
#             time.sleep(900)

def reply_to_mention(api, tweet, keywords):
    """Reply to a non-reply mention containing any of the keywords."""
    try:
        if tweet.user.id == api.me().id or tweet.in_reply_to_status_id:
            return None
        text = tweet.text.lower()
        print(f'Checking tweet {tweet.id} by @{tweet.user.screen_name}...')
        if not keywords or any(keyword.lower() in text for keyword in keywords):
            print(f'\n\nReplying to tweet {tweet.id} by @'
                  f'{tweet.user.screen_name}...')
            status = (f'@{tweet.user.screen_name} Zero To Mastery, ZTMBot to'
                      ' the rescue!\nzerotomastery.io/')
            api.update_status(status=status,
                              in_reply_to_status_id=tweet.id_str,
                              auto_populate_reply_metadata=True)
            print('Replied to', tweet.user.screen_name)
            time.sleep(900)
    except tweepy.TweepError as e:
        print("Error replying", e)


def reply_to_mentions_since_id(api, keywords, since_id) -> int:
    """Get new since_id after replying to mentions."""
    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items():
        since_id = max(tweet.id, since_id)
        reply_to_mention(api, tweet=tweet, keywords=keywords)
    return since_id

# Define a check_mentions function that accepts api, keywords, and since_id, follow and reply to the user if user has mentioned us
# def check_mentions(api, keywords, since_id):
#     new_since_id = since_id
#     for tweet in tweepy.Cursor(api.mentions_timeline,
#                                since_id=since_id).items():
#         new_since_id = max(tweet.id, new_since_id)
#         try:
#             if tweet.in_reply_to_status_id is not None:
#                 # Tweet is a reply
#                 break
#             elif any(keyword in tweet.text for keyword in keywords):
#                 status = '@' + tweet.user.screen_name + \
#                 ' Zero To Mastery, ZTMBot to the rescue! zerotomastery.io/'
#                 api.update_status(
#                 status=status, in_reply_to_status_id=tweet.id_str)
#                 print('replied to', tweet.user.screen_name)
#                 time.sleep(900)
#             else:
#                 pass
#         except tweepy.TweepError as e:
#             print("Error replying", e)
#     return new_since_id

# Define a main function to connect to the api and create a since_id counter, call all above functions


def main():
    api = create_api()
    # reply_since_id = 1
    # since_id = 1
    while True:
        # check_mentions(api, ["ZtmBot", "ztmBot", "@ZtmBot"], since_id)
        follow_followers(api)
        # unfollow(api)
        # reply_to_mentions_since_id(api, ["ZtmBot", "ztmBot", "@ZtmBot"], reply_since_id)
        time.sleep(60)


if __name__ == "__main__":
    main()
