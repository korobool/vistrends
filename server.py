import asyncio
import json

import motor.motor_asyncio
from aiohttp import web

from config import config

dbapi_string = config['db']
client = motor.motor_asyncio.AsyncIOMotorClient(dbapi_string)
db = client.analytics

async def handler(request):
    times = await request.json()
    response = web.Response(content_type='application/json')
    val1 = int(times['time_low'])
    val2 = int(times['time_high'])
    docs = []
    cursor = db.points.find({'time': {'$gt': val1, '$lt': val2}})
    for document in await cursor.to_list(length=50000):
        docs.append(document['datapoints'])
    response.text = json.dumps(docs)
    return response

async def init(loop):
    handler = app.make_handler()
    srv = await loop.create_server(handler, '0.0.0.0', 8080)
    print('serving on', srv.sockets[0].getsockname())
    return srv


loop = asyncio.get_event_loop()
app = web.Application()
app.router.add_post('/', handler)
loop.run_until_complete(init(loop))

if __name__ == '__main__':
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass