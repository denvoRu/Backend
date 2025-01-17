from datetime import time
from pydantic import BaseModel

class ScheduleTime(BaseModel):
    start: time
    end: time