from faker import Faker

fake = Faker()


# users/params.py
from dataclasses import dataclass
from typing import Literal, Optional
from common.base_params import PaginationParams, SortParams

@dataclass
class GetUsersParams(PaginationParams, SortParams):
    search: Optional[str] = None
    sort_by: Optional[Literal["created_at", "username", "display_name"]] = None


@dataclass
class GetUserPostsParams(PaginationParams, SortParams):
    ...
