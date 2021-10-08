from pandas import DataFrame
from tweepy import Cursor
import numpy as np
import tweepy
import string
import emoji
import re
import os

# Using config
# from decouple import config

# Using dotenv
from dotenv import load_dotenv
load_dotenv()

# Using os/env.py
# import env

# Authentication and connection to Twitter API.
# Using config
# consumer_key = config("CONSUMER_KEY")
# consumer_secret = config("CONSUMER_SECRET")
# access_token = config("ACCESS_TOKEN")
# access_token_secret = config("ACCESS_TOKEN_SECRET")

# Using dotenv/env.py
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def cleanTweets(text):
    # text = re.sub("https*\S+", " ", text)
    # text = re.sub("@\S+", " ", text)
    text = re.sub("https*\S+", "", text)
    text = re.sub("@\S+", "", text)
    text = emoji.demojize(text)
    # text = re.sub(r'[^\w]', ' ', text)
    # text = [char for char in text if char not in string.punctuation]
    text = ''.join(text)
    return text


def main():

    # insert the keyword here for the extraction to continue
    retweet_filter = '-filter:retweets'

    # append the term to search parameters
    q = retweet_filter
    tweets_per_qry = 200
    since_id = None
    max_id = -1
    max_tweets = 1000
    all_tweets = []

    # Usernames whose tweets we want to gather.
    users = [
        'falan4j',
    ]

    # giving the user some feed back that the script is running
    print("Tweets Extractor is starting")

    # extract tweets from timeline of targeted politicians of the major political parties
    try:

        # loop through all the users and extract tweets from their relative timelines
        for user in users:

            print("Downloading %s's tweets:" % user)

            tweets = api.user_timeline(screen_name=user,
                                       # 200 is the maximum allowed count
                                       count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       # Necessary to keep full_text
                                       # otherwise only the first 140 words are extracted
                                       tweet_mode='extended'
                                       )

            all_tweets = []
            all_tweets.extend(tweets)
            oldest_id = tweets[-1].id

            while True:
                tweets = api.user_timeline(screen_name=user,
                                           # 200 is the maximum allowed count
                                           count=200,
                                           exclude_replies=True,
                                           include_rts=False,
                                           max_id=oldest_id - 1,
                                           # Necessary to keep full_text
                                           # otherwise only the first 140 words are extracted
                                           tweet_mode='extended'
                                           )
                if len(tweets) == 0:
                    break

                oldest_id = tweets[-1].id
                all_tweets.extend(tweets)
                print('N of {0} tweets downloaded till now: {1}'.format(
                    user, len(all_tweets)))

            # Transform the tweepy tweets into a 2D array that will populate the csv
            outtweets = [[
                tweet.id_str,
                tweet.created_at,

                # Clean tweets (remove symbols, links and emojis)
                cleanTweets(tweet.full_text.encode(
                            "utf-8").decode("utf-8"))

                # Raw tweets
                # tweet.full_text.encode("utf-8").decode("utf-8")
            ]
                for idx, tweet in enumerate(all_tweets)]

            df = DataFrame(outtweets, columns=["ID", "Date Created", "Text"])

            # Remove any rows with empty strings
            df.replace(r'^\s*$', np.nan, inplace=True, regex=True)
            df.dropna(how="any", axis=0, inplace=True)
            # df.to_csv('csv/collected/%s_tweets.csv' % user, index=False)
            df.to_csv('%s_tweets.csv' % user, index=False)
            df.head(3)

            # print("Wrote {0} tweets of {1} to CSV file\n".format(
            #     len(all_tweets), user))
            print("Raw number of {0}'s tweets collected: {1}".format(
                user, len(all_tweets)))
            print("Filtered number of {0}'s tweets written to CSV: {1}\n".format(
                user, len(df.index)))

    except tweepy.TweepError as e:
        print("There was an error, find details below, else check your internet connection or your " +
              " credentials in the credentials.py file \n")
        print("If this is not your first time running this particular script, then there is a possibility that the "
              "maximum rate limit has been exceeded. wait a few more minutes and re run the script.\n")
        print(f"Error Details: {str(e)}")


if __name__ == "__main__":
    main()
