import json

from dataclasses import dataclass
from hashlib import sha256

@dataclass
class DeviceInfo:
    alias: str
    version: str
    device_model: str
    device_type: str
    fingerprint: str
    port: int 
    protocol: str
    download: bool
    announcement: bool
    announce: bool

    @property
    def json(self) -> str:
        data_dict = {
            "alias": self.alias,
            "version": self.version,
            "deviceModel": self.device_model,
            "deviceType": self.device_type,
            "fingerprint": self.fingerprint,
            "port": self.port,
            "protocol": self.protocol,
            "download": self.download,
            "announcement": self.announcement,
            "announce": self.announce
        }
        return json.dumps(data_dict)

@dataclass
class FileModel:
    id: str
    name: str
    size: int
    path: str
    created: float

    def __init__(self, name, size, path,created):
        self.id = self.calculate_hash(name)
        self.name = name
        self.size = size
        self.path = path
        self.created = created

    @staticmethod
    def calculate_hash(input_string):
        """
        计算字符串的SHA-256哈希值。
        
        参数:
        input_string (str): 输入字符串
        
        返回:
        str: SHA-256哈希值的十六进制表示
        """
        hash_object = sha256(input_string.encode())
        return hash_object.hexdigest()
    
    @property
    def content(self):
        with open(self.path, 'rb') as f:
            return f.read()

class Pagination(object):

    def __init__(self,resutls,pageN=0,pageSize=10,pagecount=0,total=0) -> None:
        self.resutls   = resutls
        self.pageN     = pageN
        self.pageSize  = pageSize
        self.pagecount = pagecount
        self.total     = total 
        self.index     = 0

    def get_pagination_bar(self):
        num = max(self.pageN,1)
        start  = 1  if num < 10  else num -5
        end    = min(10 if num < 10  else num+10 // 2 ,self.pagecount)        
        return range(start,end+1)
    
    def get_next_page(self):
        return min(self.pageN + 1,self.pagecount)
    
    def get_up_page(self):
        return max(self.pageN - 1,1)
    
    def is_current_page(self,number):
        return self.pageN == number

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.resutls):
            result = self.resutls[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
    
    @property
    def pageInfo(self):
        return {"page_info":{"page_no":self.pageN,
                        "page_size":self.pageSize,
                        "page_total":self.pagecount}}