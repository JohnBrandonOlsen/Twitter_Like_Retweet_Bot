#A script to like and retweet Tweets from selected accounts and friends.

import configparser
import json
import os
import random

import tweepy

def login():

    config = configparser.ConfigParser()
    config.read('/path/to/account.config')

    consumer_key = config['Twitter']['api_key']
    consumer_secret = config['Twitter']['api_secret']
    access_token = config['Twitter']['access_token']
    access_token_secret = config['Twitter']['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    return api

def find_most_recent(account):

    try:
        with open('/path.to/' + account + '.txt', 'r') as f:
            most_recent = f.read()
    except FileNotFoundError:
        with open('/path/to/' + account + '.txt', 'w') as f:
            most_recent = None

    return most_recent

def update_most_recent(account, last_tweet):

    with open('/path/to/' + account + '.txt', 'w') as f:
        f.write(str(last_tweet))

def LRT(api, tweets):

    for tweet in tweets:
        try:
            api.retweet(tweet.id)
            api.create_favorite(tweet.id)
        except tweepy.error.TweepError:
            continue

def add_tweets(tweets, tweet_list):

    for tweet in tweets:
        tweet_list.append(tweet)

    return tweet_list

def RT(api, tweet):

    try:
        api.retweet(tweet.id)
    except tweepy.error.TweepError:
        pass

def like(api, tweets):

    for tweet in tweets:
        try:
            api.create_favorite(tweet.id)
        except tweepy.error.TweepError:
            continue

def main():

    api = login()

    accounts =  json.loads(open('/path/to/accounts-mandatory.json').read())

    for account in accounts:
        most_recent = find_most_recent(account)

        if most_recent != None and most_recent != "":
            tweets = api.user_timeline(account, since_id = most_recent)
        else:
            tweets = api.user_timeline(account)

        if len(tweets) > 0:
            LRT(api, tweets)
            update_most_recent(account, tweets[0].id)

    accounts = json.loads(open('/path/to/accounts-discretionary.json').read())

    tweet_list = []
    for account in accounts:
        most_recent = find_most_recent(account)

        if most_recent != None and most_recent != "":
            tweets = api.user_timeline(account, since_id = most_recent)
        else:
            tweets = api.user_timeline(account)

        if len(tweets) > 0:
            like(api, tweets)
            tweet_list = add_tweets(tweets, tweet_list)

    if len(tweet_list) > 9:
        random.seed(os.urandom(1064))
        RT_num = random.randint(1,len(tweet_list))

        for i in range(RT_num):
            random.seed(os.urandom(1064))
            tweet = tweet_list[random.randint(0,len(tweet_list) - 1)]
            RT(api, tweet)

        for account in accounts:
            most_recent = find_most_recent(account)
            tweets = api.user_timeline(account)
            update_most_recent(account, tweets[0].id)

if __name__ == '__main__':
    main()
