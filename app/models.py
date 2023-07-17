from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal
from app.db import get_db

class Sport(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str
    slug: str
    active: bool

class Event(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str
    slug: str
    active: bool
    type: Literal['preplay', 'inplay']
    sport: Sport
    status: Literal['Pending', 'Started', 'Ended', 'Cancelled']
    scheduled_start: datetime
    actual_start: Optional[datetime] = Field(default=None)

    @validator("sport", pre=True)
    @classmethod
    def validate_event(cls, sport):
        query = "SELECT * FROM sports WHERE id = %s"

        with get_db() as conn:
            with conn.cursor() as cursor:
                if isinstance(sport, dict) and "id" in sport:
                    cursor.execute(query, (sport["id"],))
                elif isinstance(sport, int):
                    cursor.execute(query, (sport,))
                else:
                    raise ValueError(f"Sport with id {sport} does not exist")

                sport_data = cursor.fetchone()
                if sport_data is not None:
                    return Sport(**sport_data)
                else:
                    raise ValueError(f"Sport with id {sport} does not exist")

class Selection(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str
    event: Event
    price: Decimal
    active: bool
    outcome: Literal['Unsettled', 'Void', 'Lose', 'Win']

    @validator("event", pre=True)
    @classmethod
    def validate_event(cls, event):
        query = "SELECT * FROM events WHERE id = %s"

        with get_db() as conn:
            with conn.cursor() as cursor:
                if isinstance(event, dict) and "id" in event:
                    cursor.execute(query, (event["id"],))
                elif isinstance(event, int):
                    cursor.execute(query, (event,))
                else:
                    raise ValueError(f"Event with id {event} does not exist")

                event_data = cursor.fetchone()
                if event_data is not None:
                    return Event(**event_data)
                else:
                    raise ValueError(f"Event with id {event} does not exist")

