# Variant: app listens on :3000 (not 8000).
# On serverless this exercises Lnar's :8000 -> :3000 socat port relay.
# Register with dockerfile_path = "variants/port3000".
FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-dev --no-emit-project -o requirements.txt \
    && pip install --no-cache-dir -r requirements.txt

COPY api.py mcp_server.py ./

EXPOSE 3000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "3000"]
