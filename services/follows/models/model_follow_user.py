from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, UUID4


class ResponseUserModel(BaseModel):
    id: Annotated[str, UUID4]
    username: str
    display_name: str
    avatar_url: Optional[str]=None
    is_verified: bool


class ResponseFollowRequestModel(BaseModel):
    id: Annotated[str, UUID4]
    follower: ResponseUserModel
    following: ResponseUserModel
    status: str
    created_at: datetime