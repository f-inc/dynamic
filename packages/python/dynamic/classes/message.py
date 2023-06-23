from dataclasses import asdict, dataclass, field
import json
from typing import Any, Dict, Optional, Union
from uuid import uuid4

from dynamic.runners.runner import RunnerConfig

class BaseMessage:
    def __init__(self, content: str, route_path: Optional[str] = None):
        self.content = content
        self.route_path = route_path
    
    def to_dict(self):
        return self.__dict__

    def to_json_dump(self):
        return json.dumps(self.to_dict())

class IncomingMessage(BaseMessage):
    def __init__(self, config: RunnerConfig, id: Optional[str] = None, *args, **kwargs):
        self.config = config
        self.id = id
        if self.id is None:
            self.id = str(uuid4())
        return super(IncomingMessage, self).__init__(*args, **kwargs)

class OutgoingMessage(BaseMessage):
    def __init__(self, *args, **kwargs):
        return super(OutgoingMessage, self).__init__(*args, **kwargs)
    
class ErrorMessage(BaseMessage):
    def __init__(self, error: Exception, *args, **kwargs):
        self.error = error
        self.trace_back = error.__traceback__

        return super(ErrorMessage, self).__init__(*args, **kwargs)
