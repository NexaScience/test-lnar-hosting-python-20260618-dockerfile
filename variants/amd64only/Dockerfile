# Variant: base image pinned to linux/amd64.
# On serverless (arm64/Graviton) this MUST fail-fast at the pre-build gate
# (_check_arm64_support -> "unsupported"). On EKS (amd64) it builds and runs fine.
# Register with dockerfile_path = "variants/amd64only".
FROM --platform=linux/amd64 python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv export --no-dev --no-emit-project -o requirements.txt \
    && pip install --no-cache-dir -r requirements.txt

COPY api.py mcp_server.py ./

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
