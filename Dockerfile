FROM python:3.12-slim

RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.toml poetry.lock ./
RUN --mount=type=cache,target=/root/.cache/pypoetry/cache \
    --mount=type=cache,target=/root/.cache/pypoetry/artifacts \
    poetry install --no-root --no-cache --no-interaction

ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONPATH="/app:${PYTHONPATH}"
COPY t2v_serve /app/t2v_serve

ARG MODEL_NAME="BAAI/bge-base-en-v1.5"
ENV MODEL_NAME=${MODEL_NAME}

RUN ["poetry", "run", "python", "./t2v_serve/download.py"]
CMD ["fastapi", "run", "./t2v_serve/app.py", "--port", "8080"]