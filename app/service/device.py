from dataclasses import dataclass

import json

from ..utils import singleton
from ..models import UrlBuilder

@dataclass
class DeviceInfo:
    alias: str
    version: str
    deviceModel: str
    deviceType: str
    fingerprint: str
    port: int 
    protocol: str
    download: str = 'false'
    announcement: str = 'true'
    announce: str = 'true'
    ip_addr: str = None

    @property
    def json(self) -> str:
        return json.dumps(self.as_dict())
    
    def as_dict(self):
        return self.__dict__
    
    @property
    def url(self):
        return UrlBuilder(self.protocol,f"{self.ip_addr}:{self.port}")

@singleton
class DeviceManager:

    def __init__(self,this_device : DeviceInfo):
        # 使用字典存储设备信息，键为设备ID，值为设备详细信息的字典
        self.devices = {}
        self.this_device = this_device
    
    def add_device(self, device : DeviceInfo):
        """
        添加设备到设备管理器。
        :param device_info: 包含设备详细信息的字典
        """
        device_id = device.fingerprint
        self.devices[device_id] = device

    def get_all_devices(self):
        """
        返回所有设备的列表。
        :return: 所有设备的列表，每个设备由设备ID和设备详细信息组成的元组
        """
        devices_list = [info for id, info in self.devices.items()]
        return devices_list
    
    def get_device(self, device_id):
        """
        根据设备ID返回设备详细信息。
        :param id: 设备ID
        :return: 包含设备详细信息的字典
        """
        if device_id in self.devices:
            return self.devices[device_id]
        return None

    def remove_device(self, device_id):
        """
        根据设备ID移除设备。
        :param device_id: 要移除的设备的唯一标识符
        """
        if device_id in self.devices:
            del self.devices[device_id]
