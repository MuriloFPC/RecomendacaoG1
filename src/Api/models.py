from pydantic import BaseModel

class RecomentationRequest(BaseModel):
    newsId: str
    userId: str

class NewsRecommended(BaseModel):
    Id: str
    Url: str
    RecomentadionSource: str

class RecomentationResponse(BaseModel):
    newsRecommended: list[NewsRecommended] = []

