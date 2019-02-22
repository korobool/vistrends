import json
import datetime
import sys
import time
import re

from os import path
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime
from optparse import OptionParser

# Variables that contains the user credentials to access Twitter API
with open('secret') as f:
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
    RTless_string = re.sub('RT @[\w|\s]+:', '', DIGITless_string)
    USERless_string = re.sub('@[\w|\s]+:', '', RTless_string)
    return USERless_string.replace('\n', '')


def preproc(tweet):
    txt = body_cleanup(tweet['text'])
    data = {'text': txt}
    if 'created_at' in tweet:
        time_struct = time.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        data['created_at'] = int(time.mktime(time_struct))
    return data


class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        if 'text' in tweet:
            data = preproc(tweet)
            print(data)
        return True

    def on_error(self, status):
        print(status)


def run(tags_list):
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(track=tags_list, languages=['en'])


if __name__ == '__main__':
    try:
        tags = sys.argv[1].split()
        print("Accepted tags:", tags)
        run(tags)
    except:
        print ('Pulling error!')
        pass
