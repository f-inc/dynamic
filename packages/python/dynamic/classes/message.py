from dataclasses import asdict, dataclass, field
import json
from typing import Any, Dict, Optional, Union
from uuid import uuid4

from dynamic.runners.runner import RunnerConfig

class BaseMessage:
    """Message Inteface to be interpreted by websocket server"""
    def __init__(self, content: str, id: Optional[str] = None):
        self.content = content
        self.id = id
        if self.id is None:
            self.id = str(uuid4())
    
    def to_dict(self):
        return self.__dict__

    def to_json_dump(self):
        return json.dumps(self.to_dict())

class ClientMessage(BaseMessage):
    """Client-side websocket message"""
    def __init__(self, config: RunnerConfig, *args, **kwargs):
        self.config = config
        return super(ClientMessage, self).__init__(*args, **kwargs)

class ServerMessage(BaseMessage):
    """Server-side websocket message"""
    def __init__(self, *args, **kwargs):
        return super(ServerMessage, self).__init__(*args, **kwargs)
    
class ErrorMessage(BaseMessage):
    """Base Error Message from websocket server"""
    def __init__(self, error: Exception, *args, **kwargs):
        self.error = str(error)
        self.error_type = error.__class__.__name__

        return super(ErrorMessage, self).__init__(*args, **kwargs)
