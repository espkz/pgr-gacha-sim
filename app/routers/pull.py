from fastapi import APIRouter
from app.models.pull import PullRequest, PullResponse
from app.services.gacha_service import GachaService

router = APIRouter()
service = GachaService()

@router.post("/pull", response_model=PullResponse)
def pull(req: PullRequest):
    return service.pull(req.patch, req.banner, req.times)
