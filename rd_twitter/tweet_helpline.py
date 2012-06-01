# -*- coding: latin-1 -*-
"""
*******************************************************************************
** Script Name: tweet_helpline.py
** Author(s):   Terrence Beach (tjbeachjr@gmail.com)
*******************************************************************************

** Description:

The script will take the tweets stored helpline tweets resource file and send
them at a specified interval.

*******************************************************************************
"""
import codecs
import os
import sys
import time
import tweepy
sys.path.append("libs")
import common


###############################################################################
# Globals
###############################################################################

# The time to wait between tweets (in hours)
TWEET_SHIFT = 4


###############################################################################
# Twitter account information for oAuthentication
###############################################################################

TWITTER_CONSUMER_KEY        = ""
TWITTER_CONSUMER_SECRET     = ""
TWITTER_ACCESS_TOKEN        = ""
TWITTER_ACCESS_TOKEN_SECRET = ""


###############################################################################
# Run the script when called from the command line
###############################################################################

def main():
    log = common.setup_logger("tweet_articles")
    
    # Log into the Twitter account
    log.info("Logging into Twitter account")
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    twitter_api = tweepy.API(auth)

    # Get the list of articles to tweet (if any)
    if not os.path.exists("HelplineStockTweetList.txt"):
        log.error("HelplineStockTweetList.txt is missing!")
        return
    try:
        infile = codecs.open("HelplineStockTweetList.txt.txt", "r", "utf8")
    except:
        infile = open("HelplineStockTweetList.txt", "r")
    tweets = []
    for line in infile:
        tweet = line.rstrip()
        tweets.append(tweet)
        
    # Tweet the articles
    log.info("Sending %i new tweets" % len(tweets))
    tweet = tweets.pop(0)
    send_tweet(log, twitter_api, "Sending first tweet - Tweet contents:", tweet)
    counter = 1
    wait_time = TWEET_SHIFT * 3600 / len(tweets)
    for tweet in tweets:
        log.info("Waiting %i minutes before sending next tweet" % (wait_time / 60))
        time.sleep(wait_time)
        send_tweet(log, twitter_api, "Sending tweet %i - Tweet contents:" % counter, tweet)
        counter += 1


def send_tweet(log, twitter_api, message, tweet):
    retry = 0
    while True:
        if retry > 9:
            log.error("Maximum number of retries reached")
            return
        try:
            log.info(message)
            log.info(tweet)
            twitter_api.update_status(tweet)
            return
        except:
            log.error("Problem sending tweet. Retrying...")
            time.sleep(5.0)
            retry += 1

if __name__ == "__main__":
    main()