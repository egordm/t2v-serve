import logging
from typing import Optional

from fastapi import FastAPI, Response, status
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel

from t2v_serve.vectorizer import Vectorizer

logger = logging.getLogger('uvicorn')

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)

vectorizer: Vectorizer


@app.on_event("startup")
def startup_event():
    global vectorizer

    vectorizer = Vectorizer()


@app.get("/.well-known/live", response_class=Response)
@app.get("/.well-known/ready", response_class=Response)
async def live_and_ready(response: Response):
    response.status_code = status.HTTP_204_NO_CONTENT


@app.get("/meta")
def meta():
    return {}


class VectorInput(BaseModel):
    text: str
    config: Optional[dict] = None


class EmbeddingOutput(BaseModel):
    text: str
    vector: list[float]
    dim: int


class ErrorOutput(BaseModel):
    error: str


@app.post("/vectors")
@app.post("/vectors/")
async def read_item(item: VectorInput, response: Response) -> EmbeddingOutput | ErrorOutput:
    try:
        vectors = await vectorizer.embed([item.text])
        vector = vectors[0].tolist()
        return EmbeddingOutput(text=item.text, vector=vector, dim=len(vector))
    except Exception as e:
        logger.exception("Something went wrong while vectorizing data")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorOutput(error=str(e))


@app.post("/vectors/batch")
@app.post("/vectors/batch/")
async def read_items(items: list[VectorInput], response: Response) -> list[EmbeddingOutput] | ErrorOutput:
    try:
        vectors = await vectorizer.embed([item.text for item in items])
        return [
            EmbeddingOutput(text=item.text, vector=vector.tolist(), dim=len(vector))
            for item, vector in zip(items, vectors)
        ]
    except Exception as e:
        logger.exception("Something went wrong while vectorizing data")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorOutput(error=str(e))
