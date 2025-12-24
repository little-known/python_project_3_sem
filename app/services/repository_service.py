import csv
import io
from pathlib import Path
from typing import Optional
from aiofile import async_open
from app.infrastructure.github_client import GitHubClient


class RepositoryService:
    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client
        self.static_dir = Path("static")
        self.static_dir.mkdir(exist_ok=True)

    def _build_query(
        self,
        lang: str,
        stars_min: int = 0,
        stars_max: Optional[int] = None,
        forks_min: int = 0,
        forks_max: Optional[int] = None
    ) -> str:
        query_parts = [f"language:{lang}"]
        
        if stars_min > 0:
            query_parts.append(f"stars:>={stars_min}")
        if stars_max is not None:
            query_parts.append(f"stars:<={stars_max}")
        if forks_min > 0:
            query_parts.append(f"forks:>={forks_min}")
        if forks_max is not None:
            query_parts.append(f"forks:<={forks_max}")
        
        return " ".join(query_parts)

    async def search_and_save(
        self,
        limit: int,
        offset: int,
        lang: str,
        stars_min: int = 0,
        stars_max: Optional[int] = None,
        forks_min: int = 0,
        forks_max: Optional[int] = None
    ) -> str:
        query = self._build_query(lang, stars_min, stars_max, forks_min, forks_max)
        repositories = await self.github_client.fetch_repositories(query, limit, offset)
        
        filename = f"repositories_{lang}_{limit}_{offset}.csv"
        filepath = self.static_dir / filename
        
        fieldnames = [
            "name",
            "full_name",
            "description",
            "stars",
            "forks",
            "language",
            "url",
            "created_at",
            "updated_at"
        ]
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for repo in repositories:
            row = {
                "name": repo.get("name", ""),
                "full_name": repo.get("full_name", ""),
                "description": (repo.get("description") or "").replace("\n", " ").replace("\r", ""),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "language": repo.get("language", ""),
                "url": repo.get("html_url", ""),
                "created_at": repo.get("created_at", ""),
                "updated_at": repo.get("updated_at", "")
            }
            writer.writerow(row)
        
        csv_content = output.getvalue()
        output.close()
        
        async with async_open(filepath, "w", encoding="utf-8") as afp:
            await afp.write(csv_content)
        
        return filename

