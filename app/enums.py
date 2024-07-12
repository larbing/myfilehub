from enum import Enum

class TaskName(Enum):

    PUSH_FILE = "push_file"


class MessageName(Enum):

    CONNECT_SUCCESS = "CONNECT_SUCCESS"
    PUSH_FILE_PROGRESS = "PUSH_FILE_PROGRESS"