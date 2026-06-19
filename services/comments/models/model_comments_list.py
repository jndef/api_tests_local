from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, UUID4, Field


class ResponseUserModel(BaseModel):
    id: Annotated[str, UUID4]
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    is_verified: bool


class ResponseCommentModel(BaseModel):
    id: Annotated[str, UUID4]
    post_id: Annotated[str, UUID4]
    author: ResponseUserModel
    content: str = Field(min_length=1, max_length=1000)
    parent_comment_id: Optional[Annotated[str, UUID4]] = None
    is_deleted: bool
    likes_count: int
    created_at: datetime
    updated_at: datetime
    is_liked: bool
    replies_count: int


class ResponseCommentsModel(BaseModel):
    items: List[ResponseCommentModel]
    total: int
    page: int
    per_page: int
    pages: int