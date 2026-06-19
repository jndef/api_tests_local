from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, UUID4


class ResponseUserModel(BaseModel):
    id: Annotated[str, UUID4]
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    is_verified: bool


class ResponseCreateMessageModel(BaseModel):
    id: Annotated[str, UUID4]
    conversation_id: Annotated[str, UUID4]
    sender: ResponseUserModel
    content: str
    image_url: Optional[str] = None
    is_deleted: bool
    created_at: datetime