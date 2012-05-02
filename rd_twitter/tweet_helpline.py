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

# The time to wait between tweets (in minutes)
TWEET_WAIT_TIME = 5

# The amount of time to wait before retrying a failed tweet (in seconds)
TWEET_RETRY_TIME = 1

# The number of times to retry after a tweet failure before giving up 
TWEET_RETRY_COUNT = 10

# The email addresses where the tweet failure alert will be sent
TWEET_FAILURE_EMAILS = []

# The SMTP server address for sending emails
SMTP_SERVER = "smtp.comcast.net"

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
    
    # Get the list helpline tweets
    file_name = os.path.join("resources", "helpline_tweets.txt")
    if not os.path.exists(file_name):
        log.error("%s file is missing" % file_name)
        return
    infile = open(file_name, "r")
    tweets = []
    for line in infile:
        tweet = line.rstrip()
        tweets.append(tweet)
    infile.close()
    
    # Tweet the helpline tweets
    log.info("Sending %i helpline tweets" % len(tweets))
    counter = 1
    retries = 0
    for tweet in tweets:
        retries = 0
        while True:
            if retries > TWEET_RETRY_COUNT:
                error_message = "Unable to send tweet %i consecutive times" % TWEET_RETRY_COUNT
                log.error(error_message)
                common.send_email(SMTP_SERVER, "pixelprojectteam@gmail.com", TWEET_FAILURE_EMAILS, "Automated Helpline Tweet Script Error", error_message)
                return
            try:
                log.info("Sending helpline tweet %i - Tweet contents:" % counter)
                log.info(tweet)
                twitter_api.update_status(tweet)
                break
            except:
                log.error("Problem sending helpline tweet %i.  Retrying in %i seconds..." % (counter, TWEET_RETRY_TIME))
                retries += 1
                time.sleep(TWEET_RETRY_TIME)
        counter += 1
        if counter == len(tweets):
            continue
        log.info("Waiting %i minutes before sending next helpline tweet" % wait_time)
        time.sleep(wait_time * 60)
    
if __name__ == "__main__":
    main()