import os.path
import time

from robyn import SubRouter,Request,Response,jsonify
from . import render_template,UPLOAD_PATH,send_file
from . import FILE_SERVICE as fileService,DEVICE_MANAGER as deviceManager,SHARE_HOST,DOWNLOAD_HOST
from .utils import *

frontend = SubRouter(__name__,prefix="/share")

@frontend.get("/:id")
async def share(req:Request):
    id = getString(req.path_params,'id')
    fileService.load()
    file = fileService.get_file_by_id(id)
    if not file:
        return Response(status_code=404,description="File not found",headers={})
    
    return render_template('share.html',file=file,share_host=SHARE_HOST,download_host=DOWNLOAD_HOST)

@frontend.post("/:id")
@frontend.options("/:id")
async def info(req:Request):    
    id = getString(req.path_params,'id')
    fileService.load()
    file = fileService.get_file_by_id(id)
    if not file:
        return Response(status_code=404,description="File not found",headers={})
    
    return jsonify(file.as_dict())

@frontend.get("/:id/name/:name")
async def downfile(req:Request):
    id = req.path_params.get('id')
    file = fileService.get_file_by_id(id)

    if not file:
        return Response(status_code=404,description="File not found",headers={})

    return send_file(file,attachment=True)

@frontend.get("/redirect/:id/name/:name")
async def redirect(req:Request):
    id = req.path_params.get('id')
    name = req.path_params.get('name')
    return Response(status_code=302,description="",headers={'Location':f"{DOWNLOAD_HOST}/share/{id}/name/{name}"})