import time

from fastapi import FastAPI

from src.Api.models import RecomentationRequest,RecomentationResponse
from src.Api.predict import GetLastedNews, GetPredictionByFaiss, GetPredictionByMab
from src.Utils.log import Log

app = FastAPI()

_logging = Log(False)

# Middleware para logar requisições
@app.middleware("http")
async def log_requests(request: RecomentationRequest, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    _logging.info(f"Requisição: {request.method} {request.url} | Tempo: {process_time:.4f}s")
    return response
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/recomendation")
async def recomendation(request: RecomentationRequest):
    response = RecomentationResponse()

    predictionLastedNews = GetLastedNews(2)
    response.newsRecommended = predictionLastedNews

    predictionNewsId = GetPredictionByFaiss(request, 2)
    response.newsRecommended.append(predictionNewsId)

    predictionMba = GetPredictionByMab(request, 2)
    response.newsRecommended.append(predictionMba)

    return response