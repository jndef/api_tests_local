from datetime import datetime
from typing import List, Optional, Annotated

from pydantic import BaseModel, UUID4, Field


class ResponseUserModel(BaseModel):
    id: Annotated[str, UUID4]
    username: str
    display_name: str
    avatar_url: Optional[str]=None
    is_verified: bool
class ResponseHashtagModel(BaseModel):
    id: Annotated[str, UUID4]
    name: str
    posts_count: int


class ResponseUserPostModel(BaseModel):
    id: Annotated[str, UUID4]
    author: ResponseUserModel
    content: str
    image_url: Optional[str]=None
    is_pinned: bool
    is_deleted: bool
    parent_id: Optional[str]
    repost_type:  Optional[str]=None
    created_at: datetime
    updated_at: datetime
    is_liked: bool
    visibility: str
    likes_count: int
    comments_count: int
    reposts_count: int
    hashtags: List[ResponseHashtagModel]= []
    created_at: datetime
    updated_at: datetime
    is_liked: bool
    is_bookmarked: bool
    user_reaction:  Optional[str]=None

class ResponseUserPostsModel(BaseModel):
    items: List[ResponseUserPostModel] = []
    total: int
    page: int
    per_page: int
    pages: int