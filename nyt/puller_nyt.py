import re
import sys
import time
import pandas as pd
import requests
import motor.motor_asyncio
import logging
import datetime

from bs4 import BeautifulSoup
from os import path
from nytimesarticle import articleAPI

from config_nyt import config

api = articleAPI('769651a3298d495aa80e97ea8fae03b2')
logging.basicConfig(filename=path.join(config['log_path'], "puller_nyt.log"),
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_articles(articles):
    news = []
    for i in articles['response']['docs']:
        dic = {}
        dic['date'] = i['pub_date'][0:10]  # cutting time of day.
        dic['atype'] = i['type_of_material']
        dic['url'] = i['web_url']
        dic['headline'] = i['headline']['main']
        dic['word_count'] = int(i['word_count'])
        news.append(dic)
    return news


def get_articles_url(begin, end):
    all_articles = []

    # Some pages might return a 'No JSON object could be decoded'
    # To keep this error from stopping the loop a try/except was used.
    for i in range(0, 100):
        try:
            # Call API method with the parameters discussed on the README file
            articles = api.search(
                fq={'source': ['The New York Times']},
                begin_date=begin,
                end_date=end,
                sort='oldest',
                page=str(i))

            # Check if page is empty
            if articles['response']['docs'] == []: break

            articles = parse_articles(articles)
            all_articles = all_articles + articles

        except Exception:

            pass

        # Avoid overwhelming the API
        time.sleep(1)

    # Copy all articles on the list to a Pandas dataframe
    articles_df = pd.DataFrame(all_articles)

    # Make sure we filter out non-news articles and remove 'atype' column
    articles_df = articles_df.drop(articles_df[articles_df.atype != 'News'].index)
    articles_df.drop('atype', axis=1, inplace=True)

    # Discard non-working links (their number of word_count is 0).
    # Example: http://www.nytimes.com/2001/11/06/world/4-die-during-police-raid-in-istanbul.html
    articles_df = articles_df[articles_df.word_count != 0]
    articles_df = articles_df.reset_index(drop=True)

    return articles_df


def scarp_articles_text(articles_df):
    # Unable false positive warning from Pandas dataframe manipulation
    pd.options.mode.chained_assignment = None

    articles_df['article_text'] = 'NaN'
    session = requests.Session()

    for j in range(0, len(articles_df)):

        url = articles_df['url'][j]
        req = session.get(url)
        soup = BeautifulSoup(req.text, 'lxml')

        # Get only HTLM tags with article content
        # Articles through 1986 are found under different p tag
        paragraph_tags = soup.find_all('p', class_='story-body-text story-content')
        if paragraph_tags == []:
            paragraph_tags = soup.find_all('p', class_=re.compile("css"))

        # Put together all text from HTML p tags
        article = ''
        for p in paragraph_tags:
            article = article + ' ' + p.get_text()

        # Copy article's content to the dataframe
        articles_df['article_text'][j] = article

    return articles_df

if __name__ == '__main__':
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)

    previous_date = yesterday.strftime("%Y%m%d")
    current_date = now.strftime("%Y%m%d")

    if len(sys.argv) == 3:
        try:
            val1 = str(sys.argv[1])
            val2 = str(sys.argv[2])
            val2 = datetime.datetime.strptime(val2, "%Y%m%d") + datetime.timedelta(days=1)
            val2 = val2.strftime("%Y%m%d")
        except TypeError:
            val1 = previous_date
            val2 = current_date
    else:
        val1 = previous_date
        val2 = current_date


    logging.info('Puller NYT started.')
    dbapi_string = config['db']
    client = motor.motor_asyncio.AsyncIOMotorClient(dbapi_string)
    db = client.analytics
    articles_frame = get_articles_url(val1, val2)
    articles_frame = scarp_articles_text(articles_frame)
    articles_frame.to_csv('articles.csv', encoding='utf-8')

    for j in range(0, len(articles_frame)):
        data = {'headline': articles_frame['headline'][j],
                'url': articles_frame['url'][j],
                'word_count': int(articles_frame['word_count'][j]),
                'date': articles_frame['date'][j],
                'article_text': articles_frame['article_text'][j]}
        db.all_nyt.insert_one(data)
    logging.info('Puller NYT finished.\n')
