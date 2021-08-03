from datetime import datetime
from typing import List, Optional
from pydantic.main import BaseModel

class Team(BaseModel):
    name: str
    account_id: Optional[str]
    team_id: Optional[str]

class Match(BaseModel):
    tour_id: str
    tour_name: str
    time: datetime
    team_1: Team
    team_2: Team
    tv: List[str]
    tweet_id: Optional[str]

class Tournament(BaseModel):
    id: str
    name: str
    date: datetime
    matches: List[Match]
    tweet_id: Optional[str]
