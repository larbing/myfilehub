
import os.path
import time
import json

from robyn import SubRouter,Request,Response,serve_file
from . import render_template,UPLOAD_PATH,deviceInfo
from . import fileService
from .utils import *
from .session import SessionManager

frontend = SubRouter(__name__,prefix="/api/localsend/v2")

sessionManager = SessionManager()

@frontend.post('/prepare-upload')
async def prepare_upload(req:Request):
    session = sessionManager.create()
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
    print(req.json())
    return deviceInfo.json

