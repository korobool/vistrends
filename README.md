## vistrends
Is a simple visualizer of what entities are discussed in Twitter for a certain historical period. Under development.

#### Prarpare a vitrualenv
Create virtual environment and install all requirements.
```terminal
mkvirtualenv -p python3.6 analytics
```

#### requirements

```terminal
pip install -r requirements.txt
sudo apt-get install python3-tk
sudo pip2 install supervisor
```
#### MongoDB 
Install MongoDB on Ubuntu 16.04 (Step1-Step4)
https://www.howtoforge.com/tutorial/install-mongodb-on-ubuntu-16.04/

Create root user.
```terminal
mongo
use admin
db.createUser({user:"admin", pwd:"admin123", roles:[{role:"root", db:"admin"}]})
```

#### Database Config

Create analytics db and create collection "all_tweets" with index "created_at".
use analytics
```terminal
db.createCollection("all_tweets")
db.all_tweets.createIndex( { "created_at": 1 } )
```

Create collection "points".
```terminal
db.createCollection("points")
```

How to enter to mongodb as root?
```terminal
mongo -u admin -p admin123 --authenticationDatabase admin
use analytics
```
Create directory 'img' for images.

#### Run software
##### To run altogether:
```
make start
```
you can stop everything with 
```
make stop
```
or check the status/control by
```
make ctl
```

##### To run software separately:
* Run puller forever.
```terminal
python puller.py
```

* Run extractor once per some time period (for example, hour) by cron.
```terminal
python extractor.py
```

* Run server forever.
```terminal
python server.py
```

#### CURL Examples

One element from bd.
```terminal
curl "http://localhost:11071/single?time=1524698967" | grep }| python -mjson.tool
```
Elements for some period.
```terminal
curl "http://localhost:11071?time_min=1524660000&time_max=1524700000" | grep }| python -mjson.tool
```

Get image by file name.
```terminal
curl "http://localhost:11071/image?img=17:20:51_25.04.2018.png"
```
