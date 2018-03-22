import aiohttp
from aiohttp import web, web_request
import threading
import json
import datetime
import time

data = []

def read_stdin():
    while True:
        all_input = input()
        for line in all_input.split("\n"):
            obj = json.loads(line.strip())
            obj["time"] = datetime.datetime.now().timestamp()
            print(obj)
        obsolete_time = datetime.datetime.now().timestamp() - 120
        while data and data[0]["time"] <= obsolete_time:
            data = data[1:]

thread = threading.Thread(target=read_stdin, args=())
thread.daemon = True
thread.start()

session = aiohttp.ClientSession()
app = web.Application()

async def get_feed(request: web_request.Request):
    min_time = request.query["time"]
    output_data = []
    for obj in data:
        if obj[time] >= min_time:
            output_data.append(obj)
    return web.Response(body=json.dumps(output_data), content_type="application/json")

app.router.add_get('/feed', get_feed)
web.run_app(app, host="0.0.0.0", port=9050)
