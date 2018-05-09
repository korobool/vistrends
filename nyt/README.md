### Extracting articles from New York Times

1. Install [nytimesarticle](https://pypi.org/project/nytimesarticle/) - fully-functional Python wrapper for the New York Times Article Search API
```bash
pip install nytimesarticle
```

2. [Get NYT API Key](https://developer.nytimes.com/signup)
```bash
769651a3298d495aa80e97ea8fae03b2
```

3. Replace file *nytimesarticle.py* in virtualenv by file from this [pull request](https://github.com/evansherlock/nytimesarticle/blob/6e769ea49f548634cace38d6baa20fd554201bb4/nytimesarticle.py)

4. Install Pandas
```bash
pip install pandas
```

5. Install BeautifulSoup and LXML parser
```bash
pip install lxml
pip install bs4
```

6. Run script for writing articles to articles.csv (YYYYMMDD)
```python
python puller2.py 20180501 20180505
```

Usefull links:

[nytimesarticle 0.1.0](https://pypi.org/project/nytimesarticle/)

[nytimesarticle.py](https://github.com/evansherlock/nytimesarticle/blob/6e769ea49f548634cace38d6baa20fd554201bb4/nytimesarticle.py)

[The New York Times Developer Network](https://developer.nytimes.com/)

[Article Search API](https://developer.nytimes.com/article_search_v2.json#/Documentation/GET/articlesearch.json)

[Text-Mining-The-New-York-Times-Articles](https://github.com/nilmolne/Text-Mining-The-New-York-Times-Articles/tree/master/Code)

[textminingnyt.py](https://github.com/nilmolne/Text-Mining-The-New-York-Times-Articles/blob/master/Code/textminingnyt.py)




