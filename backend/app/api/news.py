from fastapi import APIRouter, Depends

from app.core.dependencies import get_news_service
from app.schemas.news import NewsSearchRequest, NewsSearchResponse
from app.services.news_service import NewsService

router = APIRouter(tags=["news"])


@router.post("/news/search", response_model=NewsSearchResponse)
def search_news(
    request: NewsSearchRequest, news_service: NewsService = Depends(get_news_service)
) -> NewsSearchResponse:
    return news_service.search(request.query, request.max_results)
