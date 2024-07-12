
from robyn import SubRouter,WebSocket,jsonify

from .service.session import SessionManager
from .models import Message
from .enums import MessageName


frontend = SubRouter(__name__)

websocket = WebSocket(frontend, "/ws")

sessionManager = SessionManager()

@websocket.on("message")
async def message(ws, msg, global_dependencies):
    pass 

@websocket.on("close")
async def close(ws):
    sessionManager.remove(ws.id)

@websocket.on("connect")
async def connect(ws):
    sesssion = sessionManager.create(ws.id)
    sesssion.set('ws',ws)

    return Message(MessageName.CONNECT_SUCCESS,{'socket_id':ws.id}).json