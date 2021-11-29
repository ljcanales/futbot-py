from datetime import datetime
from typing import List, Optional
from pydantic.main import BaseModel
from abc import ABCMeta, abstractmethod

class Team(BaseModel):
    name: str
    account_id: Optional[str]
    team_id: Optional[str]
    img_url: Optional[str]
    hashtag: str

class Match(BaseModel):
    tour_id: str
    tour_name: str
    time: datetime
    team_1: Team
    team_2: Team
    tv: List[str]
    tweet_id: Optional[str]
    story_posted: bool = False

class Tournament(BaseModel):
    id: str
    name: str
    date: datetime
    matches: List[Match]
    tweet_id: Optional[str]
    story_posted: bool = False

class ConfigData(BaseModel):
    send_match_message: bool = False
    tweet_match: bool = False
    post_story_match: bool = False
    update_config: bool = True

class BotModel(metaclass=ABCMeta):
    @abstractmethod
    def update(self):
        pass
