# Dockerfile detection — test matrix

One repo, many Dockerfiles. `dockerfile_path` (a repo-level setting) selects which
one to use, so every case below runs on the **same production branch** — just change
the repository settings (`dockerfile_path`, `is_serverless`) and re-deploy.

> Use a **fresh analyze-and-deploy**, not redeploy: redeploy may reuse the cached
> experiment, so a changed `dockerfile_path` might not take effect (known TODO).

| `dockerfile_path` | `is_serverless` | What it exercises | Expected result |
| --- | --- | --- | --- |
| `""` (empty) | either | no path → auto-generate | Lnar generates a Dockerfile |
| `Dockerfile` | serverless | root file, single-stage, :8000 | builds & runs; no relay (already 8000) |
| `variants/port3000` | serverless | app on :3000 | builds; `:8000 → :3000` socat relay injected |
| `variants/port3000` | EKS | app on :3000 | builds; port used directly, no relay |
| `variants/amd64only` | serverless | base pinned `linux/amd64` | **fail-fast** before build (arm64 unsupported) |
| `variants/amd64only` | EKS | base pinned `linux/amd64` | builds & runs (amd64) |
| `variants/alias` | either | final stage `FROM base` (alias) | builds; final-stage base resolves through alias |
| `variants/distroless` | serverless | distroless final stage | **fail-fast** before build (no shell for relay) |
| `variants/buildkit` | either | `RUN --mount=` (BuildKit-only) | build **fails naturally** in Kaniko (not pre-detected) |
| `does/not/exist` | either | path missing in the commit | **fail-fast** "Dockerfile not found" |

All variants build the same app (`api.py` + `mcp_server.py`) from the repo root as
the build context.
