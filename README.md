## vistrends
Is a simple visualizer of what entities are discussed in Twitter for a certain historical period. Under development.

#### Prarpare a vitrualenv
Create virtual environment and install all requirements.
```
mkvirtualenv -p Python3.6 analytics
```

#### requirements

```
pip install -r requirements.txt
```
#### MongoDB 
Install MongoDB on Ubuntu 16.04 (Step1-Step4)
https://www.howtoforge.com/tutorial/install-mongodb-on-ubuntu-16.04/

Create root user.
```
mongo
use admin
db.createUser({user:"admin", pwd:"admin123", roles:[{role:"root", db:"admin"}]})
```

#### Database Config

Create analytics db and create collection "all_tweets" with index "created_at".
use analytics
```
db.createCollection("all_tweets")
db.all_tweets.createIndex( { "created_at": 1 } )
```

Create collection "points".
```
db.createCollection("points")
```

How to enter to mongodb as root?
```
mongo -u admin -p admin123 --authenticationDatabase admin
use analytics
```
Create directory 'img' for images.

#### Run software

Run puller forever.
```
python puller.py
```

Run extractor once per some time period (for example, hour) by cron.
```
python extractor.py
```

Run server forever.
```
python server.py
```

#### CURL Examples

One element from bd.
```
curl "http://localhost:8080/single?time=1524698967" | grep }| python -mjson.tool
```
Elements for some period.
```
curl "http://localhost:8080?time_min=1524660000&time_max=1524700000" | grep }| python -mjson.tool
```

Get image by file name.
```
curl "http://localhost:8080/image?img=17:20:51_25.04.2018.png"
```
