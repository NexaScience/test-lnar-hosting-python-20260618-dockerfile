# Variant: multi-stage where the final stage's FROM references an earlier AS alias
# (`FROM base`). Exercises final-stage base resolution (_final_base_stage alias loop):
# the runtime arch/base must resolve through the alias to python:3.13-slim.
# Register with dockerfile_path = "variants/alias".
FROM python:3.13-slim AS base

WORKDIR /app

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-dev --no-emit-project -o requirements.txt \
    && pip install --no-cache-dir -r requirements.txt

FROM base AS final

COPY api.py mcp_server.py ./

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
