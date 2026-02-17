from pydantic import BaseModel
from typing import Optional, List

class PullRequest(BaseModel):
    patch: str
    banner: str
    times: int


class PullResult(BaseModel):
    name: str
    rarity: int
    banner: Optional[List[str]] = None
    img: str


class PullResponse(BaseModel):
    banner: str
    results: list[PullResult]