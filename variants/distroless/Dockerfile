# Variant: distroless final stage (no shell / no package manager).
# On serverless this MUST fail-fast (_base_lacks_shell) because the :8000 socat
# relay layer cannot be injected. This is a fail-fast FIXTURE — it is only meant
# to verify the serverless block, not to run a working server.
# Register with dockerfile_path = "variants/distroless" and deploy as serverless.
FROM python:3.13-slim AS builder

WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-dev --no-emit-project -o requirements.txt \
    && pip install --no-cache-dir --target=/site-packages -r requirements.txt
COPY api.py mcp_server.py ./

FROM gcr.io/distroless/python3-debian12

WORKDIR /app
ENV PYTHONPATH=/site-packages
COPY --from=builder /site-packages /site-packages
COPY --from=builder /app/api.py /app/mcp_server.py ./

EXPOSE 8000
CMD ["api.py"]
