import socket
import time
import threading

class MulticastService:
    def __init__(self,deviceInfo):
        self.MCAST_GRP = '224.0.0.167'
        self.MCAST_PORT = 53317
        self.deviceInfo = deviceInfo
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def broadcast(self):
        msg = self.deviceInfo.json.encode()
        self.send_sock.sendto(msg, (self.MCAST_GRP, self.MCAST_PORT))

    def _loop(self):
        while True:
            try:
                self.broadcast()
            except Exception as e:
                print(e)
            finally:
                time.sleep(15)

    def start(self):
        t = threading.Thread(target=self._loop)
        t.start()