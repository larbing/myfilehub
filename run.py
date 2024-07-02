from robyn import Robyn 

app = Robyn(__file__)

from app import index,api
from app import STATIC_PATH,deviceInfo
from app.broadcast import ServiceBroadcast

async def startup_handler():
    service_broadcast = ServiceBroadcast(deviceInfo)
    service_broadcast.start()

app.startup_handler(startup_handler)
app.include_router(index.frontend)
app.include_router(api.frontend)
app.add_directory(
        route="/static",
        directory_path=STATIC_PATH,
)
app.start(port=8080,host="0.0.0.0")