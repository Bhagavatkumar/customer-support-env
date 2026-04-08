from pydantic import BaseModel
from typing import List, Optional


class Observation(BaseModel):
    ticket_id: str
    message: str
    history: List[str]
    step_count: int


class Action(BaseModel):
    action_type: str
    content: Optional[str] = None


class Reward(BaseModel):
    value: float
