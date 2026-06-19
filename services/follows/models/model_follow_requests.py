from datetime import datetime
from typing import List, Annotated, Optional

from pydantic import BaseModel, UUID4


class ResponseUserModel(BaseModel):
    id: Annotated[str, UUID4]
    username: str
    display_name: str
    avatar_url: Optional[str]=None
    is_verified: bool


class ResponseFollowerModel(BaseModel):
    id: Annotated[str, UUID4]
    follower: ResponseUserModel
    status: str
    created_at: datetime


class ResponseFollowersListModel(BaseModel):
    items: List[ResponseFollowerModel]
    total: int
    page: int
    per_page: int
    pages: int