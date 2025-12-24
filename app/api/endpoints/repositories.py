from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from app.services.repository_service import RepositoryService
from app.infrastructure.github_client import GitHubClient

router = APIRouter()


@router.get("/repositories")
async def search_repositories(
    limit: int = Query(..., gt=0, le=1000),
    offset: int = Query(0, ge=0),
    lang: str = Query(...),
    stars_min: int = Query(0, ge=0),
    stars_max: Optional[int] = Query(None, ge=0),
    forks_min: int = Query(0, ge=0),
    forks_max: Optional[int] = Query(None, ge=0)
):
    github_client = GitHubClient()
    service = RepositoryService(github_client)
    
    try:
        filename = await service.search_and_save(
            limit=limit,
            offset=offset,
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max
        )
        return {"status": "success", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

