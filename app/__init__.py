import os
import pathlib
import uuid

from robyn import Response
from robyn.templating import JinjaTemplate
from .services import FileService
from .models import DeviceInfo

current_file_path = pathlib.Path(__file__).parent.resolve()
JINJA_TEMPLATE = JinjaTemplate(os.path.join(current_file_path, "templates"))

STATIC_PATH = os.path.join(current_file_path, "static")

UPLOAD_PATH = os.getenv('UPLOAD_PATH')

fileService = FileService(UPLOAD_PATH)

deviceInfo = DeviceInfo(
    alias="server",
    version="2.0",
    device_model="headless",
    device_type="headless",
    fingerprint=str(uuid.uuid4()),
    port=8080,
    protocol="http",
    download=False,
    announcement=True,
    announce=True
)


def render_template(template_name, **kwargs):
    return JINJA_TEMPLATE.render_template(template_name, **kwargs)

def send_file(file):
    return Response(status_code=200,description=file.content,
                    headers={"Content-Disposition": "attachment"} )