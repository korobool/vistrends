import json
import asyncio
import aiohttp
import motor.motor_asyncio
import logging

from os import path
from aiohttp import web
from os import path
from PIL import Image
from io import BytesIO
from config import config

dbapi_string = config['db']
port = config['serving_at']
client = motor.motor_asyncio.AsyncIOMotorClient(dbapi_string)
db = client.analytics

logging.basicConfig(filename=path.join(config['log_path'], "server.log"),
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def handler(request):
    logging.info('Multiple response.')
    val1 = int(request.rel_url.query['time_min'])
    val2 = int(request.rel_url.query['time_max'])
    response = web.Response(content_type='application/json')
    docs = []
    cursor = db.points.find({'time': {'$gt': val1, '$lt': val2}})
    for document in await cursor.to_list(length=50000):
        docs.append({'time': document['time'],
                     'datapoins': document['datapoints'],
                     'img_path': document['img']})
    response.text = json.dumps(docs)
    return response


async def handler_single(request):
    logging.info('Single response.')
    val = int(request.rel_url.query['time'])
    response = web.Response(content_type='application/json')
    document = await db.points.find_one({'time': val})
    response.text = json.dumps({'time': document['time'],
                                'datapoins': document['datapoints'],
                                'img_path': document['img']})
    return response


async def handler_image(request):
    logging.info('Image response.')
    t = str(request.rel_url.query['img'])
    img_path = path.join(d, config['img_path'], t)
    with BytesIO() as output:
        with Image.open(img_path) as img:
            img.save(output, 'PNG')
        im = output.getvalue()
    response = web.Response(body=im, content_type='image/png')
    return response


async def init(loop):
    handler = app.make_handler()
    srv = await loop.create_server(handler, '0.0.0.0', port)
    sock = srv.sockets[0].getsockname()
    print('Serving on', sock)
    logging.info('Server started on ' + str(sock))
    return srv


d = path.dirname(__file__)
loop = asyncio.get_event_loop()
app = web.Application()
app.router.add_get('/', handler)
app.router.add_get('/single', handler_single)
app.router.add_get('/image', handler_image)
loop.run_until_complete(init(loop))

if __name__ == '__main__':
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    logging.info('Server stopped.\n')
