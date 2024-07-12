import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import mimetypes

import json
import requests

from dataclasses import dataclass

from robyn import Robyn
app = Robyn(__file__)

from app import DEVICE_MANAGER as deviceManager,FILE_SERVICE as fileService

from app.service.file import FileSender
from app.service.device import DeviceInfo

target_drive = DeviceInfo(
    alias="oneplus6",
    version="2.0",
    deviceModel="OnePlus",
    deviceType="mobile",
    fingerprint= "DF40F7D9A1EDAF37507DD056B8CBB5B378B35064FF5501E102703636D47DE91B",
    port=53317,
    protocol="https",
    ip_addr="192.168.200.211",
)