# Variation 1: root Dockerfile, single-stage, listens on :8000 (serverless-ready).
FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

# Install dependencies from the locked manifest (no project install needed).
COPY pyproject.toml uv.lock ./
RUN uv export --no-dev --no-emit-project -o requirements.txt \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
