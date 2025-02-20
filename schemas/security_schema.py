from typing import Literal

from pydantic import BaseModel

from datetime import datetime


class OAuth2Response(BaseModel):
    access_token: str
    expires_in: datetime
    user_name: str
    user_id: int

    token_type: Literal["bearer"] = "bearer"
