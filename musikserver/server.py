#!/usr/bin/env python3

import asyncio
import spotbox
import credentials
from aiohttp.web import Application, Response, MsgType, WebSocketResponse, HTTPFound

@asyncio.coroutine
def wshandler(request):
    resp = WebSocketResponse()
    ok, protocol = resp.can_prepare(request)
    if not ok:
        return HTTPFound('/index.html')

    yield from resp.prepare(request)
    print('Client connected.')
    request.app['sockets'].append(resp)

    while True:
        msg = yield from resp.receive()
        if msg.tp == MsgType.text:
            box.command([s.strip() for s in msg.data.split(",")])
        else:
            break

    request.app['sockets'].remove(resp)
    print('Someone disconnected.')
    return resp

@asyncio.coroutine
def redirect(request):
    return HTTPFound('/index.html')

@asyncio.coroutine
def init(loop):
    app = Application(loop=loop)
    app['sockets'] = []
    app.router.add_route('GET', '/ws', wshandler)
    app.router.add_route('GET', '/', redirect)
    app.router.add_static('/', '../ui/static')
    handler = app.make_handler()
    srv = yield from loop.create_server(handler, '127.0.0.1', 8080)
    print("Server started at http://127.0.0.1:8080")
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

box = spotbox.Spotbox(credentials.username, credentials.password)
box.start()

loop = asyncio.get_event_loop()
app, srv, handler = loop.run_until_complete(init(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(finish(app, srv, handler))