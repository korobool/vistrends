import aiohttp
from aiohttp import web, web_request
import json
import datetime
import sys
import motor.motor_asyncio

from config import config

dbapi_string = config['db']

client = motor.motor_asyncio.AsyncIOMotorClient(dbapi_string)
db = client['test_database']

session = aiohttp.ClientSession()
app = web.Application()

def get_min_max_time(request: web_request.Request, time_min_default, time_min_limit=None):
    if "min_time" in request.query:
        query_min_time = int(request.query["min_time"])
        if time_min_limit:
            min_time = max(query_min_time, datetime.datetime.now().timestamp() - time_min_limit)
        else:
            min_time = query_min_time
    else:
        min_time = datetime.datetime.now().timestamp() - time_min_default
    if "max_time" in request.query:
        query_max_time = int(request.query["max_time"])
        max_time = max(query_max_time, datetime.datetime.now().timestamp())
    else:
        max_time = max(datetime.datetime.now().timestamp())
    return min_time, max_time

async def get_trends(request: web_request.Request):
    min_time, max_time = get_min_max_time(request, -86400)
    docs = await db.test_collection.find_all({'time': {'$gt': min_time, "$lt": max_time}})
    return web.Response(body=json.dumps(docs), content_type="application/json")

async def get_updates(request: web_request.Request):
    min_time, max_time = get_min_max_time(request, -120)
    docs = await db.test_collection.find_all({'time': {'$gt': min_time, "$lt": max_time}})
    return web.Response(body=json.dumps(docs), content_type="application/json")

app.router.add_get('/feed_updates', get_updates)
web.run_app(app, host="0.0.0.0", port=9050)
