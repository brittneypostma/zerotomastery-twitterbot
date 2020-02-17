# This file will use the Tweepy Cursor API to reply to mentions, follow users that follow us, and a backup like and retweet
# imports tweepy, time, and the create_api function from config.py
from typing import List

import tweepy
import time
from config import create_api


def follow_followers(api):
    """Follow users following the bot."""
    for follower in tweepy.Cursor(api.followers).items():
        try:
            print(f'{follower.name} follows the bot...')
            if not follower.following:
                follower.follow()
                print('Followed ', follower.name)
        except tweepy.RateLimitError:
            print("Rate Limit Exceeded")
            time.sleep(900)


def unfollow_non_followers(api):
    """Unfollow if a followed user is no longer following."""
    for friend in tweepy.Cursor(api.friends).items():
        try:
            print(f'Currently following {friend.name}...')
            friendship = api.show_friendship(source_id=api.me().id_str,
                                             target_id=friend.id_str)[1]
            if not friendship.following:
                api.destroy_friendship(id=friend.id_str)
                print(f'Unfollowed {friend.name} :(')
                time.sleep(10)
        except tweepy.RateLimitError:
            print("Rate Limit Exceeded")
            time.sleep(900)


def reply_to_mention(api, tweet, keywords):
    """Reply to a non-reply mention containing any of the keywords."""
    try:
        if tweet.user.id == api.me().id:
            return None
        text = tweet.text.lower()
        print(f'Checking tweet {tweet.id}...')
        if tweet.in_reply_to_status_id is None and any(
                keyword.lower() in text for keyword in keywords):
            print(f'\n\nReplying to tweet {tweet.id}...')
            status = (f'@{tweet.user.screen_name} Zero To Mastery, ZTMBot to'
                      ' the rescue!\nzerotomastery.io/')
            api.update_status(status=status, in_reply_to_status_id=tweet.id_str)
            print('Replied to', tweet.user.screen_name)
            time.sleep(10)
    except tweepy.TweepError as e:
        print("Error replying", e)


def reply_to_mentions_since_id(api, keywords, since_id) -> int:
    """Get new since_id after replying to mentions."""
    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items():
        since_id = max(tweet.id, since_id)
        reply_to_mention(api, tweet=tweet, keywords=keywords)
    return since_id


def favorite_tweet(tweet) -> None:
    """Like tweet if not liked by bot."""
    try:
        if not tweet.favorited:
            tweet.favorite()
            print("I have liked the tweet")
    except tweepy.TweepError as e:
        print(e.reason)


def retweet_tweet(tweet) -> None:
    """Retweet if bot has not retweeted tweet."""
    try:
        if not tweet.retweeted:
            tweet.retweet()
            print('Retweeted the tweet')
    except tweepy.TweepError as e:
        print(e.reason)


def fav_retweet_since_id(api, keywords, since_id) -> int:
    """Search for tweets with a search criteria and like tweet if not
     liked by the bot and retweet if not retweeted by the bot.
    """
    for tweet in tweepy.Cursor(api.search, keywords, since_id=since_id).items(
            100):
        try:
            since_id = max(tweet.id, since_id)
            favorite_tweet(tweet)
            retweet_tweet(tweet)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break
    return since_id


def main():
    api = create_api()
    reply_since_id = 1
    fav_since_id = 1
    reply_keywords = ['MagicandcodeB']#["ZtmBot", "ztmBot", "@ZtmBot"]
    fav_keywords = ['magicandcode']#["#ZTM", "#Zerotomastery", "#ztm", "zerotomastery",
              #"ZeroToMastery", "Andrei Neagoie", "Yihua Zhang", "Daniel Bourke"]
    while True:
        follow_followers(api)
        unfollow_non_followers(api)
        print('Try since_id....')
        reply_since_id = reply_to_mentions_since_id(api,
                                                    keywords=reply_keywords,
                                                    since_id=reply_since_id)
        fav_since_id = fav_retweet_since_id(api,
                                            keywords=fav_keywords,
                                            since_id=fav_since_id)
        print('reply_since_id: ', reply_since_id)
        print('fav_since_id: ', fav_since_id)
        # fav_retweet(api)
        print('Waiting for next poll...')
        time.sleep(60)


if __name__ == "__main__":
    main()
