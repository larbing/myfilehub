
import datetime
import threading

def getInt(values,key,default=0):
    value = values.get(key)
    try: 
        return max(int(value),default)
    except:
        return default

def getString(values,key,default=None):
    value = values.get(key)
    try: 
        return str(value)
    except:
        return default

def timestamp():
    return int(datetime.datetime.now().timestamp())


def synchronized(func):
    """线程安全的装饰器"""
    func.__lock__ = threading.Lock()

    def wrapper(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return wrapper

def singleton(cls):
    """单例模式装饰器"""
    instances = {}

    @synchronized
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance