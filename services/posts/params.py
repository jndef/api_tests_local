from faker import Faker
from pydantic import UUID4

fake = Faker()


# users/params.py
from dataclasses import dataclass
from typing import Literal, Optional, Annotated
from common.base_params import PaginationParams, SortParams, BaseParams



@dataclass
class GetPostsParams(PaginationParams, SortParams):
    hashtag: Optional[str] = None
    author_id: Annotated[str, UUID4] = None
    sort_by: Optional[Literal["created_at", "likes_count", "comments_count"]] = None


@dataclass
class GetFeedParams(PaginationParams):
    ...

@dataclass
class DeletePostParams(BaseParams):
    reason: Optional[str] = None
