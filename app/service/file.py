
import json
import mimetypes
import os
import requests
import asyncio

from dataclasses import dataclass
from hashlib import sha256

from ..utils import timestamp
from ..models import Pagination, UrlBuilder

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
        self.type = mimetypes.guess_type(name)[0]
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
    
    def chunked(self,chunk_size=1024):
        with open(self.path, 'rb') as file:
            num = 0
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                num += len(chunk)
                yield (num, chunk)

    def as_dict(self):
        return {
            "id": self.id,
            "fileName": self.name,
            "size": self.size,
            "fileType": self.type,
        }

class FileService:
    def __init__(self, base_path):
        self.base_path = base_path
        self.files = self._load_files()  # 加载文件列表

    def _load_files(self):
        """
        初始化时加载base_path下所有文件的列表。
        
        返回:
        list: 包含FileModel对象的列表
        """
        files_list = []
        for filename in os.listdir(self.base_path):
            if os.path.isfile(os.path.join(self.base_path, filename)):
                file_path = os.path.join(self.base_path, filename)
                file_size = os.path.getsize(file_path)
                file_time = os.path.getctime(file_path)
                files_list.append(FileModel(filename, file_size, file_path,file_time))

        return sorted(files_list, key=lambda x: x.created, reverse=True)
        
    def list_files(self, page_size=10, current_page=1):
        """
        返回指定目录下的所有文件对象（FileModel）列表，支持分页。
        
        参数:
        page_size (int): 每页显示的文件数量，默认为10
        current_page (int): 当前页码，默认为1
        
        返回:
        list: 包含目录下所有文件对象的列表，按分页规则返回
        """
        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        total = len(self.files)
        page_count = total // page_size + (1 if total % page_size > 0 else 0)
        return Pagination(self.files[start_index:end_index], current_page, page_size, page_count, total)
         
    def get_file_by_id(self, file_id):
        """
        根据ID返回FileModel对象。
        
        参数:
        file_id (str): 文件的ID
        
        返回:
        FileModel: 与给定ID匹配的文件对象，若不存在则返回None
        """
        for file in self.files:
            if file.id == file_id:
                return file
        return None
    
    def write_to_file(self, binary_data, file_name):
        file_path = os.path.join(self.base_path, file_name)
        with open(file_path, "wb") as file:
            file.write(binary_data)
        return FileModel(file_name, len(binary_data), file_path, timestamp())

    def save_files(self, files:dict[str, bytes]):
        for file_name, binary_data in files.items():
            saved_file = self.write_to_file(binary_data, file_name)
            self.files.insert(0, saved_file)

class ApiUrl:

    def __init__(self, builder:UrlBuilder):
        self.builder = builder

    def build_prepare_upload_url(self):
        return self.builder.build("/api/localsend/v2/prepare-upload")
    
    def build_upload_url(self,sessionId,fileId,file_token):
        return self.builder.build("/api/localsend/v2/upload",
                                  {'sessionId':sessionId,'fileId':fileId,'token':file_token})

class FileSender:
    def __init__(self, target_device, this_device):
        self.api = ApiUrl(target_device.url)
        self.this_device = this_device
    
    async def prepare_upload(self, file):
        req = {}
        req['info']  = self.this_device.as_dict()
        req['files'] = {file.id: file.as_dict()}

        resp = requests.post(self.api.build_prepare_upload_url(), verify=False, json=req)
        resp.raise_for_status()  # 检查响应状态码，如果不是200，则抛出异常
        
        session = resp.json()
        sessionId = session['sessionId']
        file_token = session['files'][file.id]
        
        return sessionId, file_token
    
    async def upload_file(self,sessionId,file,file_token, upload_progress=None):

        def read_chunked():
            for num,chunk in file.chunked():
                if upload_progress:
                    upload_progress(num)
                yield chunk

        upload_url = self.api.build_upload_url(sessionId, file.id, file_token)
        resp = requests.post(upload_url, verify=False, data=read_chunked())
        resp.raise_for_status()  # 再次检查响应状态码
        
        return resp.status_code
    
    async def send_file(self, file):
        session_id, task = await self.create_send_file_task(file)
        return await asyncio.gather(task)
        
    async def create_send_file_task(self, file, send_file_progress=None):
        session_id, file_token = await self.prepare_upload(file)
        task = asyncio.create_task(self.upload_file(session_id, file, 
                                                    file_token,
                                                    upload_progress=send_file_progress))
        return session_id,task
