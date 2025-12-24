import httpx
from typing import Dict, List, Any


class GitHubClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }

    async def search_repositories(
        self,
        query: str,
        page: int = 1,
        per_page: int = 100
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/search/repositories"
            params = {
                "q": query,
                "page": page,
                "per_page": per_page,
                "sort": "stars",
                "order": "desc"
            }
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()

    async def fetch_repositories(
        self,
        query: str,
        limit: int,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        repositories = []
        current_page = (offset // 100) + 1
        start_index = offset % 100
        remaining = limit

        while remaining > 0:
            data = await self.search_repositories(query, current_page, 100)
            
            items = data.get("items", [])
            if not items:
                break

            end_index = start_index + remaining
            available_items = items[start_index:end_index]
            repositories.extend(available_items)
            
            remaining -= len(available_items)
            
            if len(items) < 100 or remaining <= 0:
                break
                
            start_index = 0
            current_page += 1

        return repositories[:limit]

