from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional

from pydantic import BaseModel, UUID4


class ReactionType(str, Enum):
    LIKE = "like"
    LOVE = "love"
    LAUGH = "laugh"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"


class ResponseUserModel(BaseModel):
    id: Annotated[str, UUID4]
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    is_verified: bool


class ResponseReactionModel(BaseModel):
    id: Annotated[str, UUID4]
    user: ResponseUserModel
    reaction: ReactionType
    created_at: datetime


class ResponsePostReactionsListModel(BaseModel):
    items: List[ResponseReactionModel]
    total: int
    page: int
    per_page: int
    pages: int