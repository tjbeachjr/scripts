# -*- coding: latin-1 -*-
"""
*******************************************************************************
** Script Name: build_tweets_from_alerts.py
** Author(s):   Terrence Beach (tjbeachjr@gmail.com)
*******************************************************************************

** Description:

Connects to the Google IMAP mail server, downloads any new Google Alert 
messages.  Once the messages are found download them, store them and parse the
emails searching for News articles.

The script will build tweets from the article and store them in a file called
new_tweets.txt.  This file will be used by the tweet_articles.py script to 
Tweet the articles using your Twitter account.  You can review the tweets in
this file and make modifications before tweeting them.

The script currently leaves the Google Alert emails in the INBOX, but marks
them as read.  You should manually delete the emails to ensure they are not
used again in the future.  In the future we can setup the script to
automatically delete the Google Alert email or move it to another folder on
the Gmail account.

*******************************************************************************
"""
import base64
import bs4
import codecs
import email
import os
import rfc822
import sys
import time
import urlparse
sys.path.append("libs")
import bitly
import common
from imap_email import Mailbox

###############################################################################
# Gmail account information
###############################################################################

EMAIL_SERVER_ADDRESS    = "imap.googlemail.com"
EMAIL_SERVER_PORT       = 993
EMAIL_ADDRESS           = ""
EMAIL_PASSWORD          = ""
EMAIL_USE_SSL           = True
EMAIL_FOLDER            = "INBOX"


###############################################################################
# Bitly account information
###############################################################################

BITLY_USERNAME = ""
BITLY_API_KEY  = ""


###############################################################################
# Run the script when called from the command line
###############################################################################

def main():
    new_articles = []
    log = common.setup_logger("build_tweets_from_alerts")
    
    # Log into the Bitly account
    bitly_api = bitly.Api(login = BITLY_USERNAME, apikey = BITLY_API_KEY)     
    
    # Connect to Gmail account
    gmail = Mailbox(EMAIL_SERVER_ADDRESS, EMAIL_SERVER_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_USE_SSL, EMAIL_FOLDER)
    if not gmail.loggedIn():
        log.error("Unable to login to Gmail account")
        return
    
    # Create a directory to store the alert emails (for future use)
    if not os.path.exists("alert_emails"):
        os.mkdir("alert_emails")
    
    # Search the Gmail INBOX for Google Alert emails
    messages = gmail.getMessages('(FROM "googlealerts-noreply@google.com")')
    if len(messages) == 0:
        log.info("No Google Alert emails available")
        return
    
    # Store and parse each of the Google Alert emails
    for message in messages:
        gmail.markAsRead(message)
        
        # Download the email and store it
        contents = gmail.downloadSingleEmail(message)
        mail_obj = email.message_from_string(contents)
        struct_time = rfc822.parsedate(mail_obj.get("Date"))
        time_str = time.strftime("%y-%m-%d_%H.%M.%S", struct_time)
        email_name = "alert_email_%s.msg" % time_str
        log.info("Downloading email and storing to %s" % email_name)
        email_file = open(os.path.join("alert_emails", email_name), "w+")
        email_file.write(contents)
        email_file.close()
        
        # Parse the email and pull out the articles
        try:
            articles = parse_email(mail_obj)
        except:
            log.error("Error parsing Google Alert email %s" % email_file)
            continue
        log.info("Found %i articles in Google Alert email" % len(articles))
        time.sleep(0.5)
        new_articles += articles
    
    # Store the articles in the new_tweets.txt file so that they can
    # be tweeted later
    outfile = codecs.open("new_tweets.txt", "w", "utf8")
    log.info("Found %i total articles in Google Alert emails" % len(new_articles))
    counter = 1
    for article in new_articles:
        short_url = bitly_api.shorten(article["link"])
        tweet = build_tweet(article, short_url)
        log.info("******************* Article %i *******************" % counter)
        log.info("Article Country: %s" % article["country"])
        log.info("Article Title:   %s" % article["title"])
        log.info("Article Link:    %s" % article["link"])
        log.info("Tweet:           %s" % tweet)
        outfile.write("%s\n" % tweet)
        counter += 1
        time.sleep(0.5)
    outfile.close()                        


"""
build_tweet
"""

def build_tweet(article, short_url):
    tweet = "#%s %s %s" % (article["country"], article["title"], short_url)
    if len(tweet) > 140:
        remove_chars = len(tweet) - 137
        new_title = article["country"][:remove_chars] + "..."
        tweet = "#%s %s %s" % (article["country"], new_title, short_url)
    return tweet


"""
parse_email

Description:

Parses the alert email.  Search the email for the text/html content.  Once
found begin parsing the html content looking for links to News articles.
"""

def parse_email(mail_obj):
    articles = []
    for part in mail_obj.walk():
        if part.get_content_type() == "text/html":
            html_content = part.get_payload().replace("=\r\n", "").replace("=3D" , "=")
            articles = parse_html_content(html_content)
            return articles
    return articles


"""
parse_html_content

Parse the HTML of the Google Alert email.  Find all the links and determine
which ones are the links for the News article.  Collect the link, the
headline and the country in a list and return it at the end.
"""
        
def parse_html_content(html_content):
    articles = []
    soup = bs4.BeautifulSoup(html_content)
    
    # Find all the links in the HTML
    for link in soup.find_all("a"):
        contents = link.contents
        attrs = link.attrs
        
        # Get the article title
        article_title = ""
        for stuff in contents:
            if isinstance(stuff, bs4.element.Tag):
                try:
                    article_title += stuff.contents[0]
                except:
                    continue
            elif isinstance(stuff, bs4.element.NavigableString):
                article_title += stuff
        
        # Determine if the link is for an article or not
        link_href = attrs["href"]
        if not link_href or not article_title:
            continue
        if article_title.find("See all stories on this topic") != -1:
            continue
        if not link.has_attr("style"):
            continue
        
        # Store the title, link and country in dictionary and add to the list
        # of articles.
        query_string = urlparse.urlparse(link_href).query
        article_link = urlparse.parse_qs(query_string)["q"][0]
        article_country = get_country_from_url(article_link)
        articles.append({"title": article_title, "link": article_link, "country": article_country})
    return articles

                        
"""
get_country_from_url

Description:

Get the domain suffix from the URL (.com, .uk, .ca, etc) and use it to get the
name of the country.
"""

def get_country_from_url(url):
    domain = urlparse.urlparse(url).netloc.split(".")[-1]
    return common.country_codes[domain.upper()]


if __name__ == "__main__":
    main()