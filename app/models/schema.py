from pydantic import BaseModel

class PullRequest(BaseModel):
    banner: str
    patch: str
    times: int