from fastapi import FastAPI
from app.api.endpoints import repositories

app = FastAPI(title="GitHub Repository Search API")

app.include_router(repositories.router, prefix="/api/v1", tags=["repositories"])


@app.get("/")
async def root():
    return {"message": "GitHub Repository Search API"}

