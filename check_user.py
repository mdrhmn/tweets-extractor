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

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.get_user('mdrhmn_')
    print("User exists")
except tweepy.TweepError as e:
    print("User does not exist")
