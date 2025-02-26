from typing import Optional
from pydantic import BaseModel

class RecomentationRequest(BaseModel):
    newsId: Optional[str] = None
    userId: Optional[str] = None
class NewsRecommended(BaseModel):
    Id: str
    Url: str
    RecomentadionSource: str

class RecomentationResponse(BaseModel):
    newsRecommended: list[NewsRecommended] = []

