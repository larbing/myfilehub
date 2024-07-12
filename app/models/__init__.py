import json
import mimetypes
from urllib.parse import urlparse, urlencode, urlunparse
from dataclasses import dataclass
from hashlib import sha256
from ..enums import MessageName

@dataclass
class Message:
    name: MessageName
    values: dict

    @property
    def json(self):
        return json.dumps({
            "name": self.name.value,
            "values": self.values
        })

class UrlBuilder:
    def __init__(self, scheme, netloc):
        self.scheme = scheme
        self.netloc = netloc

    def build(self,path,query_params={}):
        query_string = urlencode(query_params)
        url = urlunparse((self.scheme, self.netloc, path, '', query_string, ''))
        return url
    
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