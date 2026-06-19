from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

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


class ResponseCommentReactionModel(BaseModel):
    id: Annotated[str, UUID4]
    user: ResponseUserModel
    reaction: ReactionType
    created_at: datetime