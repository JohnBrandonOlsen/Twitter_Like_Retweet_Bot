#A script to like and retweet Tweets from selected accounts and friends.

import tweepy
import configparser
import json

def login():

    config = configparser.ConfigParser()
    config.read('/home/pi/HoopersCreek/account.config')

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
        with open('/path/to/' + account + '.txt', 'r') as f:
            most_recent = f.read()
    except FileNotFoundError:
        with open('/path/to/' + account + '.txt', 'w') as f:
            most_recent = None

    return most_recent

def update_most_recent(account, last_tweet):

    with open('/path/to/' + account + '.txt', 'w') as f:
        f.write(str(last_tweet))

def LRT(api, account, most_recent):

    if most_recent != None and most_recent != "":
        tweets = api.user_timeline(account, since_id = most_recent)
    else:
        tweets = api.user_timeline(account)

    if len(tweets) > 0:

        for tweet in tweets:
            try:
                api.retweet(tweet.id)
                api.create_favorite(tweet.id)
            except tweepy.error.TweepError:
                continue

        last_tweet = tweets[0].id

        update_most_recent(account, last_tweet)

def main():

    api = login()

    accounts =  json.loads(open('/path/to/accounts.json').read())

    for account in accounts:
        most_recent = find_most_recent(account)
        LRT(api, account, most_recent)

if __name__ == '__main__':
    main()
