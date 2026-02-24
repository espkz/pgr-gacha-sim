from pydantic import BaseModel
from typing import Optional, List

class PullRequest(BaseModel):
    patch: str
    banner: str
    times: int


class PullResult(BaseModel):
    name: str
    rarity: int
    rank: Optional[str] = None
    unit: Optional[str] = None
    banner: Optional[List[str]] = None
    img: str
    offpity: Optional[List[str]] = None


class PullResponse(BaseModel):
    banner: str
    results: list[PullResult]