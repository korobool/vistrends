import aiohttp
import json
import datetime
import sys
import motor.motor_asyncio

import re

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from config import config

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
    RTless_string = re.sub('RT @[\w|\s]+:', '', DIGITless_string)
    USERless_string = re.sub('@[\w|\s]+:', '', RTless_string)
    return USERless_string.replace('\n', '')


def preproc(tweet):
    txt = body_cleanup(tweet['text'])
    data = {'text': txt, 'src': 'twitter'}
    if 'coordinates' in tweet:
        data['coordinates'] = tweet['coordinates']
    if 'place' in tweet:
        data['place'] = tweet['place']
    if 'created_at' in tweet:
        data['created_at'] = tweet['created_at']
    to_prn = json.dumps(data)
    return to_prn


class Writter(object):
    def __init__(self, db):
        self._db = db

    def put(self, data):
        self.all_tweets.insert(data)


class StdOutListener(StreamListener):
    writer = None

    def on_data(self, data):
        tweet = json.loads(data)
        if 'text' in tweet:
            item = preproc(tweet)
            self.writer.put(item)
            print('{}'.format(item))

        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    dbapi_string = config['db']
    client = motor.motor_asyncio.AsyncIOMotorClient(dbapi_string)
    db = client['all_tweets']

    listener = StdOutListener()
    listener.writer = Writter(db)

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    #
    # # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['news', 'socialmedia'], languages=['en'])
