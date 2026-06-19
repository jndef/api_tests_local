from pydantic import BaseModel, UUID4
from typing import List, Optional, Annotated


class ResponseUserModel(BaseModel):
    id: Annotated[str, UUID4]
    username: str
    display_name: str
    avatar_url: Optional[str]=None
    is_verified: bool


class ResponseUserItemsModel(BaseModel):
    items: List[ResponseUserModel] = []
    total: int
    page: int
    per_page: int
    pages: int