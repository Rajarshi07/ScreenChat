import socketio
BACKEND_URL = 'http://localhost:8000'
VISIBLE = True
PAUSE = False
MSG_RECORD = True
MSG = None
WINDOW = None
NAME = "user"
MESSAGE = []
HISTORY = []
HISTORYIDX = -1
ROOM = "room1"

SIO = socketio.Client()


@SIO.event
def connect():
    print("connection established")
    SIO.emit('join_room', ROOM)

@SIO.event
def disconnect():
    print("disconnected from server")

