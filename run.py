import multiprocessing
import os

from robyn import Robyn 

app = Robyn(__file__)

from app import index,api,ws,share
from app import STATIC_PATH,DEVICE_MANAGER as deviceManager
from app.service.multicast import MulticastService

async def startup_handler():
    service_broadcast = MulticastService(deviceManager.this_device)
    service_broadcast.start()

app.add_directory(
        route="/static",
        directory_path=STATIC_PATH,
)

def server():
    app.startup_handler(startup_handler)
    app.include_router(index.frontend)
    app.include_router(api.frontend)
    app.include_router(ws.frontend)
    app.start(port=8080,host="0.0.0.0")

def share_server():
    app.include_router(share.frontend)
    app.start(port=8081,host="0.0.0.0")

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=server)
    p1.start()

    p2 = multiprocessing.Process(target=share_server)
    p2.start()