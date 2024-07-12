import uuid

from ..utils import singleton,synchronized

class SimpleSession:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.data = {}

    def get_session_id(self):
        return self.session_id

    def set(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)

    def delete(self, key):
        if key in self.data:
            del self.data[key]

    def clear(self):
        self.data.clear()

@singleton
class SessionManager:
    def __init__(self):
        self.sessions = {}

    @synchronized
    def new(self):
        new_session = SimpleSession()
        self.sessions[new_session.get_session_id()] = new_session
        return new_session

    @synchronized
    def create(self,session_id):
        new_session = SimpleSession()
        new_session.session_id = session_id
        self.sessions[new_session.get_session_id()] = new_session
        return new_session

    def get(self, session_id):
        return self.sessions.get(session_id)

    def remove(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
