from dotenv import load_dotenv
from pandas import DataFrame
import pandas as pd
import numpy as np
import tweepy
import time
import json
import csv
import os

load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_followers(screen_name):
    print('Getting followers list of', screen_name)
    followers = []
    followers_screenNames = []
    users = tweepy.Cursor(api.followers, screen_name='@' +
                          screen_name, wait_on_rate_limit=True, count=200)
    for user in users.items():
        try:
            followers.append(user)
            followers_screenNames.append(user.screen_name)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)

    print('Fetched number of followers for '+screen_name+' : ', len(followers))
    return followers, followers_screenNames


def get_following(screen_name):
    print('Getting followings list of', screen_name)
    friends = []
    friends_screenName = []
    users = tweepy.Cursor(api.friends, screen_name='@'+screen_name,
                          wait_on_rate_limit=True, count=200)
    for user in users.items():
        try:
            friends.append(user)
            friends_screenName.append(user.screen_name)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    print('Fetched number of following for '+screen_name+' : ', len(friends))
    return friends, friends_screenName


def fetch_data(username):

    followers_list = list(get_followers(username))[0]
    following_list = list(get_following(username))[0]
    followers_data = []
    following_data = []

    for user in followers_list:
        try:
            print('Fetching data of', user.name)
            ob = {
                'ID': user.id,
                'Twitter Username': user.screen_name,
                'Twitter Name': user.name,
                'Tweets Count': user.statuses_count,
                'Followers Count': user.followers_count,
                'Followings Count': user.friends_count,
                # 'Followers':list(get_followers(user.screen_name))[1],
                # 'Following':list(get_following(user.screen_name))[1],
            }
            # print(ob)
            followers_data.append(ob)
            print('Data saved, moving on to next user\n')

        except Exception as ex:
            print(ex)
            pass

    for user in following_list:
        try:
            print('Fetching data of', user.name)
            ob = {
                'ID': user.id,
                'Twitter Username': user.screen_name,
                'Twitter Name': user.name,
                'Tweets Count': user.statuses_count,
                'Followers Count': user.followers_count,
                'Followings Count': user.friends_count,
                # 'Followers':list(get_followers(user.screen_name))[1],
                # 'Following':list(get_following(user.screen_name))[1],
            }
            # print(ob)
            following_data.append(ob)
            print('Data saved, moving on to next user\n')

        except Exception as ex:
            print(ex)
            pass

    keys = followers_data[0].keys()
    csv_name = str(username) + "_followers.csv"
    with open(csv_name, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(followers_data)

    keys = following_data[0].keys()
    csv_name = str(username) + "_following.csv"
    with open(csv_name, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(following_data)


fetch_data('mdrhmn_')
