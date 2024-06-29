import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from sentence_transformers import SentenceTransformer

from t2v_serve.settings import Settings

logger = logging.getLogger('uvicorn.vectorizer')


class Vectorizer():
    _executor: ThreadPoolExecutor
    _model: SentenceTransformer

    def __init__(self):
        super().__init__()
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._model = SentenceTransformer(Settings.model_name)

        logger.info(f"SentenceVectorizer initialized")

    async def embed(self, texts: list[str]) -> list[np.ndarray]:
        return await self._aembed_batch(texts)

    async def _aembed_batch(self, texts: list[str]) -> list[np.ndarray]:
        return await asyncio.wrap_future(
            self._executor.submit(self._embed_batch, texts)
        )

    def _embed_batch(self, texts: list[str]) -> list[np.ndarray]:
        result: np.ndarray = self._model.encode(
            sentences=texts,
            batch_size=Settings.batch_size,
            convert_to_numpy=True,
        )

        return list(result)
