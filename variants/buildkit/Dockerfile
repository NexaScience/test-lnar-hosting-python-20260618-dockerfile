# Variant: BuildKit-only syntax (`RUN --mount=...`).
# Lnar does NOT pre-detect this (TODO(buildkit)); the Kaniko build is expected to
# FAIL naturally during the build step (no early gate). Use this to confirm the
# failure is surfaced (not silently ignored).
# Register with dockerfile_path = "variants/buildkit".
FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/pip \
    uv export --frozen --no-dev --no-emit-project -o requirements.txt \
    && pip install -r requirements.txt

COPY api.py mcp_server.py ./

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
