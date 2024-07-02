
import os

from .models import FileModel,Pagination
from .utils import timestamp


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