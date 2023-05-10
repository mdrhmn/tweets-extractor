from pandas import DataFrame
import numpy as np
import tweepy
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

# Using .env file
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def tweets_extractor(usernames: list):

    TWEETS_PER_QUERY = 500
    MAX_ID = -1

    # Giving the user some feed back that the script is running
    print("Tweets Extractor is starting")

    # extract tweets from timeline of targeted politicians of the major political parties
    try:

        # loop through all the users and extract tweets from their relative timelines
        for username in usernames:

            print("Downloading %s's tweets:" % username)

            # Declare API call function
            tweets = api.user_timeline(
                screen_name=username,
                # 200 is the maximum allowed count
                count=TWEETS_PER_QUERY,
                exclude_replies=False,
                include_rts=False,
                # Necessary to keep full_text
                # otherwise only the first 140 words are extracted
                tweet_mode="extended",
            )

            all_tweets = []
            all_tweets.extend(tweets)
            oldest_id = tweets[MAX_ID].id

            while True:
                # Declare API call function
                tweets = api.user_timeline(
                    screen_name=username,
                    # 200 is the maximum allowed count
                    count=TWEETS_PER_QUERY,
                    max_id=oldest_id - 1,
                    exclude_replies=True,
                    include_rts=False,
                    # Necessary to keep full_text
                    # otherwise only the first 140 words are extracted
                    tweet_mode="extended",
                )
                if len(tweets) == 0:
                    break

                oldest_id = tweets[MAX_ID].id
                all_tweets.extend(tweets)
                print(
                    "N of {0} tweets downloaded till now: {1}".format(
                        username, len(all_tweets)
                    )
                )

            # Transform the tweepy tweets into a 2D array that will populate the csv
            outtweets = [
                [
                    tweet.id_str,
                    tweet.created_at,
                    tweet.lang,
                    tweet.is_quote_status,
                    # Raw tweets
                    tweet.full_text.encode("utf-8").decode("utf-8"),
                ]
                for idx, tweet in enumerate(all_tweets)
            ]

            # df = DataFrame(outtweets, columns=[
            #                "ID", "Date Created", "Text"])

            df = DataFrame(
                outtweets,
                columns=["ID", "Date Created", "Lang", "Quote Status", "Text"],
            )

            # Remove any rows with empty strings
            df.replace(r"^\s*$", np.nan, inplace=True, regex=True)
            df.dropna(how="any", axis=0, inplace=True)
            df.to_csv("%s_tweets.csv" % username, index=False)
            print(
                "Raw number of {0}'s tweets collected: {1}".format(
                    username, len(all_tweets)
                )
            )
            print(
                "Filtered number of {0}'s tweets written to CSV: {1}\n".format(
                    username, len(df.index)
                )
            )

    except AttributeError as e:
        print(f"Error Details: {str(e)}")


tweets_extractor(usernames=[""])
