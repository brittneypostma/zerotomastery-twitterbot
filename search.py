# This file will use the Tweepy Cursor API to reply to mentions, follow users that follow us, and a backup like and retweet
# imports tweepy, time, and the create_api function from config.py

# Define a check_mentions function that accepts api, keywords, and since_id, follow and reply to the user if user has mentioned us

# Define a follow_followers function that accepts api and check if they are not followed, then follow them

# Define a fav_retweet function that accepts api, create terms string to search for and use the tweepy.Cursor object to search those terms 100 times
# Check if not favorited and retweeted, and then favorite or retweet, catch errors

# Define a main function to connect to the api and create a since_id counter, call all above functions

# if __name__ main, call the main function
