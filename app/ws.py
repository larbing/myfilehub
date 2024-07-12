
from robyn import SubRouter,WebSocket,jsonify

from .service.session import SessionManager


frontend = SubRouter(__name__)

websocket = WebSocket(frontend, "/ws")

sessionManager = SessionManager()

@websocket.on("message")
async def message(ws, msg, global_dependencies):
    print(msg)
    return "{}"

@websocket.on("close")
async def close(ws):
    print("close")
    sessionManager.remove(ws.id)
    return

@websocket.on("connect")
async def connect(ws):
    print("connect")

    sesssion = sessionManager.create(ws.id)
    sesssion.set('ws',ws)

    msg = {}
    msg['msg_name'] = 'connect_success'
    msg['socket_id'] = ws.id

    return jsonify(msg)