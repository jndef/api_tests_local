from pydantic import UUID4



# users/params.py
from dataclasses import dataclass
from typing import Literal, Optional, Annotated
from common.base_params import PaginationParams, SortParams, BaseParams


@dataclass
class GetCommentsParams(PaginationParams, SortParams):
    post_id: Annotated[str, UUID4] = None
    sort_by: Optional[Literal["created_at", "likes_count"]] = None


@dataclass
class GetRepliesParams(PaginationParams):
    comment_id : Annotated[str, UUID4] = None
    sort_by: Optional[Literal["created_at", "likes_count"]] = None
