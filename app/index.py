
import os.path
import time

from robyn import SubRouter,Request,Response
from . import render_template,UPLOAD_PATH,send_file
from . import FILE_SERVICE as fileService,DEVICE_MANAGER as deviceManager
from .utils import *

frontend = SubRouter(__name__)


@frontend.get("/")
async def index(req:Request):
    page = getInt(req.query_params,'page',1)
    file_list = fileService.list_files(current_page=page)
    device_list = deviceManager.get_all_devices()
    return render_template('file.html',file_list=file_list,time=time,device_list=device_list)

@frontend.get("/file/:id/name/:name")
async def downfile(req:Request):
    id = req.path_params.get('id')
    file = fileService.get_file_by_id(id)
    if not file:
        return Response(status_code=404,description="File not found",headers={})
    
    return send_file(file)

@frontend.post("/upload")
async def upload(req:Request):
    files = req.files
    fileService.save_files(files)
    return Response(status_code=200,description="Upload success",headers={})

