import os
import pathlib
import uuid

from robyn import Response
from robyn.templating import JinjaTemplate
from .service.file import FileService
from .service.device import DeviceInfo,DeviceManager

current_file_path = pathlib.Path(__file__).parent.resolve()
JINJA_TEMPLATE = JinjaTemplate(os.path.join(current_file_path, "templates"))

STATIC_PATH = os.path.join(current_file_path, "static")

UPLOAD_PATH = os.getenv('UPLOAD_PATH')

FILE_SERVICE = FileService(UPLOAD_PATH)

SHARE_HOST = os.getenv('SHARE_HOST')
DOWNLOAD_HOST = os.getenv('DOWNLOAD_HOST')

DEVICE_MANAGER = DeviceManager(DeviceInfo(
    alias="server",
    version="2.0",
    deviceModel="headless",
    deviceType="headless",
    fingerprint=str(uuid.uuid4()),
    port=8080,
    protocol="http",
))

def render_template(template_name, **kwargs):
    return JINJA_TEMPLATE.render_template(template_name, **kwargs)

def send_file(file,bytes_limit=0,attachment=False):
    content = file.content[:bytes_limit] if bytes_limit > 0 else file.content
    return Response(status_code=200,description=content,
                    headers={"Content-Disposition": "attachment" if attachment else file.type} )