from  pydantic import BaseModel
from typing import Optional, Literal

class LogoutResponse(BaseModel):
    detail: Literal["Not authenticated"]
