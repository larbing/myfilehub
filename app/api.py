
import os.path
import time
import json
import asyncio

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from robyn import SubRouter,Request,Response,serve_file,jsonify
from . import render_template,UPLOAD_PATH
from . import FILE_SERVICE as fileService,DEVICE_MANAGER as deviceManager
from .utils import *
from .service.session import SessionManager
from .service.device import DeviceInfo
from .service.file import FileSender
from .enums import TaskName,MessageName
from .models import Message

frontend = SubRouter(__name__,prefix="/api/localsend/v2")

sessionManager = SessionManager()

@frontend.post('/prepare-upload')
async def prepare_upload(req:Request):
    print(req.json())
    session = sessionManager.new()
    results = {'sessionId':session.get_session_id()}
    results['files'] = {}

    files = json.loads(req.json().get('files'))
    for key in files:
        file = files[key]
        session.set(file['id'],file['fileName'])
        results['files'][file['id']] = file['fileName']

    return results

@frontend.post('/upload')
async def upload(req:Request):
    sessionId = getString(req.query_params,'sessionId')
    fileId = getString(req.query_params,'fileId')

    session = sessionManager.get(sessionId)
    if not session:
        return Response(status_code=403,description="Session not found",headers={})
    
    fileName = session.get(fileId)
    if not fileName:
        return Response(status_code=404,description="File not found",headers={})
    
    if isinstance(req.body,list):
        req.body = bytes(req.body)

    elif isinstance(req.body,str):
        req.body = req.body.encode()
    
    file = {fileName:req.body}
    fileService.save_files(file)
    sessionManager.remove(sessionId)

    return Response(status_code=200,description="Upload success",headers={})

@frontend.post('/register')
async def register(req:Request):
    new_device = DeviceInfo(**req.json())
    new_device.ip_addr = req.ip_addr
    deviceManager.add_device(new_device)
    return deviceManager.this_device.json


def push_file_progress(socket_id):
    socket_session = sessionManager.get(socket_id)
    if not socket_session:
        return None
    
    def progress(num):
        ws = socket_session.get("ws")
        if not ws:
            print("Could not find websocket :{}",socket_id)
            return False

        message = Message(MessageName.PUSH_FILE_PROGRESS,{'total_bytes':num})
        ws.sync_send_to(socket_id, message.json)
        return True

    return progress

@frontend.post("/push")
async def push(req:Request):

    device_id = getString(req.json(),'deviceId')
    file_id   = getString(req.json(),'fileId')
    socket_id = getString(req.json(),'socketId')

    target_device = deviceManager.get_device(device_id)
    if not target_device:
        return Response(status_code=404,description="Device not found",headers={})
    
    file = fileService.get_file_by_id(file_id)
    if not file:
        return Response(status_code=404,description="File not found",headers={})
    
    session_id = None
    try:
        sender = FileSender(target_device, deviceManager.this_device)
        progress = push_file_progress(socket_id)
        session_id,task = await sender.create_send_file_task(file,send_file_progress=progress)
        session = sessionManager.create(session_id)
        session.set(TaskName.PUSH_FILE,task)
        await asyncio.gather(task)

        return Response(status_code=200,description="success",headers={})
    
    except Exception as e:
        return Response(status_code=500,description=str(e),headers={})

    finally:
        sessionManager.remove(session_id)

@frontend.post("/cancel")
async def cancel(req:Request):
    session_id = getString(req.query_params,'sessionId')
    session = sessionManager.get(session_id)
    
    if not session:
        return Response(status_code=404,description="Session not found",headers={})
    
    try:
        task = session.get(TaskName.PUSH_FILE)
        if task:
            task.cancel()
    finally:
        sessionManager.remove(session_id)

    return Response(status_code=200,description="success",headers={})
    
    