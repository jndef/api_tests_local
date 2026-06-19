from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, UUID4


class ResponseUserModel(BaseModel):
    id: Annotated[str, UUID4]
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    is_verified: bool


class ResponseHashtagModel(BaseModel):
    id: Annotated[str, UUID4]
    name: str
    posts_count: int


class ResponsePostModel(BaseModel):
    id: Annotated[str, UUID4]
    author: ResponseUserModel
    content: str
    image_url: Optional[str] = None
    is_pinned: bool
    is_deleted: bool
    parent_id: Optional[Annotated[str, UUID4]] = None
    repost_type: Optional[str] = None
    visibility: str
    likes_count: int
    comments_count: int
    reposts_count: int
    hashtags: Optional[List[ResponseHashtagModel]] = []
    created_at: datetime
    updated_at: datetime
    is_liked: bool
    is_bookmarked: bool
    user_reaction: Optional[str] = None


class ResponseBookmarksModel(BaseModel):
    items: List[ResponsePostModel] = []
    total: int
    page: int
    per_page: int
    pages: int