from fastapi import APIRouter, HTTPException, BackgroundTasks
from backend.services.scraper import ScraperService
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()
scraper_service = ScraperService()

class ScrapedDocument(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    content: Optional[str] = None
    source: str

class ScrapeResponse(BaseModel):
    status: str
    count: int
    data: List[ScrapedDocument]

@router.post("/scrape", response_model=ScrapeResponse)
async def trigger_scrape():
    """
    Trigger the web scraper to fetch university program data.
    Note: For a production system with 50+ pages, this should be a background task.
    For MVP verification, we run it synchronously (or use BackgroundTasks if it times out).
    Given the deep scraping might take > 30s, let's keep it sync for immediate feedback 
    BUT limit the scope or warn. 
    Actually, let's run it and return the data directly for Story 2.2 verification verification.
    """
    try:
        results = scraper_service.scrape_all_programs()
        return {
            "status": "success",
            "count": len(results),
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
