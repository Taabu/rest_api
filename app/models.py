from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

class Sport(BaseModel):
    id: int
    name: str
    slug: str
    active: bool

class Event(BaseModel):
    id: int
    name: str
    slug: str
    active: bool
    type: Literal['preplay', 'inplay']
    sport: Sport
    status: Literal['Pending', 'Started', 'Ended', 'Cancelled']
    scheduled_start: datetime.datetime
    actual_start: Optional[datetime.datetime]

class Selection(BaseModel):
    id: int
    name: str
    event: Event
    price: Decimal
    active: bool
    outcome: Literal['Unsettled', 'Void', 'Lose', 'Win']
