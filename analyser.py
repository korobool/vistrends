import sys
import pprint
import asyncio
import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://admin:fend183Er@localhost:27017/tracking?authSource=admin')
db = client.analytics

async def do_find(val1, val2):
    cursor = db.all_tweets.find({'created_at': {'$gt': val1, '$lt': val2}})
    for document in await cursor.to_list(length=10000):
        pprint.pprint(document)
        print(document['created_at'])
        print(document['text'])
        print('***************************')

if __name__ == '__main__':
    val1 = float(sys.argv[1])
    val2 = float(sys.argv[2])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_find(val1, val2))