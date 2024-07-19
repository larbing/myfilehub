
import os.path
import time

from robyn import SubRouter,Request,Response
from . import render_template,UPLOAD_PATH,send_file
from . import FILE_SERVICE as fileService,DEVICE_MANAGER as deviceManager,SHARE_HOST
from .utils import *

frontend = SubRouter(__name__)


@frontend.get("/")
async def index(req:Request):
    return render_template('index.html')

@frontend.get("/file-list")
@frontend.get("/file-list/:path")
async def list(req:Request):
    page = getInt(req.query_params,'page',1)
    type = getString(req.path_params,'path','')

    def filter_func(file):
        if type == 'videos':
            return file.is_video()
        elif type == 'images':
            return file.is_image()
        elif type == 'documents':
            return file.is_text()
        else:
            return True

    pagination = fileService.list_files(current_page=page,filter_func=filter_func)
    device_list = deviceManager.get_all_devices()
    return render_template('list.html',pagination=pagination,
                           time=time,device_list=device_list,type=type,SHARE_HOST=SHARE_HOST)

@frontend.get("/device-list")
def device_list(req:Request):
    device_list = deviceManager.get_all_devices()
    return render_template('device.html',device_list=device_list)

@frontend.post("/upload")
async def upload(req:Request):
    files = req.files
    fileService.save_files(files)
    return Response(status_code=200,description="Upload success",headers={})

@frontend.post("/update-context")
async def update_context(req:Request):
    file_id   = getString(req.json(),'fileId')
    context = getString(req.json(),'context')

    file = fileService.get_file_by_id(file_id)
    if not file:
        return Response(status_code=200,description="文件不存在",headers={})
    
    if not context: 
        return Response(status_code=200,description="内容不能空",headers={})
    
    if not file.is_text():
        return Response(status_code=200,description="只能更新文本文件",headers={})

    fileService.write_to_file(context.encode(), file.name)
    return Response(status_code=200,description="更新成功",headers={})

@frontend.get("/file/:id/name/:name")
async def downfile(req:Request):
    id = req.path_params.get('id')
    file = fileService.get_file_by_id(id)
    limit = getInt(req.headers,'content-bytes-limit',0)

    if not file:
        return Response(status_code=404,description="File not found",headers={})

    return send_file(file,bytes_limit=limit)