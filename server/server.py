from aiohttp import web
import socketio
from datetime import datetime

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    """Serve the client-side application."""
    with open("server/index.html") as f:
        return web.Response(text=f.read(), content_type="text/html")


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def message(sid, data):
    print("message ", data,sid)
    msg = {
        'msg':data['msg'],
        'room':data['room'],
        # 'ts':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'name':data['name']
        # 'sid':sid
    }
    await sio.emit('message',msg, room=data['room'], skip_sid=sid)

@sio.event
def join_room(sid,data):
    sio.enter_room(sid, data)

@sio.event
def exit_room(sid,data):
    sio.leave_room(sid, data)

@sio.event
def disconnect(sid):
    print("disconnect ", sid)


# app.router.add_static("/static", "static")
app.router.add_get("/", index)

if __name__ == "__main__":
    web.run_app(app,host='127.0.0.1',port=8000)
