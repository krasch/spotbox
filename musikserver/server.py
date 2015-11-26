#!/usr/bin/env python3

import json
import yaml
import asyncio
from aiohttp.web import Application, Response, MsgType, WebSocketResponse, HTTPFound

import spotbox

@asyncio.coroutine
def wshandler(request):
    resp = WebSocketResponse()
    ok, protocol = resp.can_prepare(request)
    if not ok:
        return HTTPFound('/index.html')

    yield from resp.prepare(request)
    print('Client connected.')
    request.app['sockets'].append(resp)
    box.command({"command": "state"})

    while True:
        msg = yield from resp.receive()
        if msg.tp == MsgType.text:
            box.command(json.loads(msg.data))
        else:
            break

    request.app['sockets'].remove(resp)
    print('Someone disconnected.')
    return resp

@asyncio.coroutine
def redirect(request):
    return HTTPFound('/index.html')

def brodcast(app, msg):
    for ws in app['sockets']:
        ws.send_str(json.dumps(msg))

def consumer_thread(app, loop):
    def inner():
        while True:
            msg = box.status_queue.get()
            loop.call_soon_threadsafe(brodcast, app, msg)
    return inner

@asyncio.coroutine
def init(loop, host, port):
    app = Application(loop=loop)
    app['sockets'] = []
    app.router.add_route('GET', '/ws', wshandler)
    app.router.add_route('GET', '/', redirect)
    app.router.add_static('/', '../ui/static')
    handler = app.make_handler()
    srv = yield from loop.create_server(handler, host, port)
    print("Server started at {}:{}".format(host, port))
    return app, srv, handler

@asyncio.coroutine
def finish(app, srv, handler):
    for ws in app['sockets']:
        ws.close()
    app['sockets'].clear()
    yield from asyncio.sleep(0.1)
    srv.close()
    yield from handler.finish_connections()
    yield from srv.wait_closed()

with open("config.yaml", 'r') as config:
    config = yaml.load(config)
    credentials = config["spotify"]
    host = config["server"]["host"]
    port = config["server"]["port"]
    buffer_size = config["audio"]["buffer_size"]

box = spotbox.Spotbox(credentials["username"], credentials["password"], buffer_size)
alsa = spotbox.Alsa(box.sound_queue)

loop = asyncio.get_event_loop()
app, srv, handler = loop.run_until_complete(init(loop, host, port))

loop.run_in_executor(None, consumer_thread(app, loop))
loop.run_in_executor(None, box.run)
loop.run_in_executor(None, alsa.run)
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(finish(app, srv, handler))
