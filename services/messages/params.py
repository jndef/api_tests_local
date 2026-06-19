from pydantic import UUID4



# users/params.py
from dataclasses import dataclass
from typing import Literal, Optional, Annotated
from common.base_params import PaginationParams


@dataclass
class GetConversationsListParams(PaginationParams):
    ...

@dataclass
class GetConversationMessagesListParams(PaginationParams):
    ...