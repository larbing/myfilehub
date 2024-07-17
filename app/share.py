import os.path
import time

from robyn import SubRouter,Request,Response
from . import render_template,UPLOAD_PATH,send_file
from . import FILE_SERVICE as fileService,DEVICE_MANAGER as deviceManager,SHARE_HOST,DOWNLOAD_HOST
from .utils import *

frontend = SubRouter(__name__,prefix="/share")

@frontend.get("/:id")
async def getfile(req:Request):
    id = getString(req.path_params,'id')
    fileService.load()
    file = fileService.get_file_by_id(id)
    if not file:
        return Response(status_code=404,description="File not found",headers={})
    
    return render_template('share.html',file=file,share_host=SHARE_HOST,download_host=DOWNLOAD_HOST)

@frontend.get("/:id/name/:name")
async def downfile(req:Request):
    id = req.path_params.get('id')
    file = fileService.get_file_by_id(id)
    limit = getInt(req.headers,'content-bytes-limit',0)

    if not file:
        return Response(status_code=404,description="File not found",headers={})

    return send_file(file,bytes_limit=limit)