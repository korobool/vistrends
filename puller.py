# Import the necessary methods from tweepy library
import re

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json

# import pandas as pd
# import matplotlib.pyplot as plt

# Variables that contains the user credentials to access Twitter API
with open('sercet') as f:
    secret = json.loads(f.read())

access_token = secret['access_token']
access_token_secret = secret['access_token_secret']
consumer_key = secret['consumer_key']
consumer_secret = secret['consumer_secret']


# This is a basic listener that just prints received tweets to stdout.
def body_cleanup(text):
    URLless_string = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' URL ', text)
    YEARless_string = re.sub(r'\s[1-9][0-9][0-9][0-9]\s', ' YEAR ', URLless_string)
    DIGITless_string = re.sub(r'[0-9]+', ' DIGIT ', YEARless_string)
    DIGITless_string = re.sub(r'DIGIT-DIGIT', ' RANGE ', DIGITless_string)
    DIGITless_string = re.sub(r'YEAR-YEAR', ' RANGE ', DIGITless_string)
    return DIGITless_string.replace('\n', '')


def preproc(tweet):
    txt = body_cleanup(tweet['text'])
    to_prn = json.dumps({'text': txt, 'src': 'twitter'})
    return to_prn


class StdOutListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        if 'text' in tweet:
            item = preproc(tweet)
            print('{}'.format(item))
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    #
    # # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['news', 'socialmedia'], languages=['en'])
