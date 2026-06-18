# test-lnar-hosting-python (Dockerfile 検知マトリクス)

ユーザー指定 Dockerfile の検知・実行を検証するためのテストリポジトリ。
アプリ本体は FastAPI + FastMCP（`api.py` / `mcp_server.py`、`/mcp` と `/health` を 1 プロセスで提供）。

1 つのリポジトリに複数の Dockerfile を置き、`dockerfile_path`（repo 単位の設定）でどれを使うかを
切り替える。すべて**同一の production ブランチ**で動かせる。

## 構成（1リポジトリ・同一 production ブランチ）

```
Dockerfile                      # baseline: 単一ステージ, :8000
variants/port3000/Dockerfile    # :3000 → serverless socat 中継
variants/amd64only/Dockerfile   # FROM --platform=linux/amd64 → serverless arm64 fail-fast
variants/alias/Dockerfile       # 最終ステージ FROM base（alias 解決）
variants/distroless/Dockerfile  # distroless 最終 → serverless fail-fast（fixture）
variants/buildkit/Dockerfile    # RUN --mount= → Kaniko 自然失敗
variants/README.md              # 設定×期待結果のマトリクス表
```

すべての variant は、ビルドコンテキスト = リポジトリルートで同じアプリ
（`api.py` + `mcp_server.py`）をビルドする。

## テスト方法（設定切替で全網羅）

`dockerfile_path` と `is_serverless` を変えて **fresh analyze-and-deploy** するだけ。

> 注意: redeploy は cached_experiment を優先するため、`dockerfile_path` を切り替えるときは
> **新規 analyze-and-deploy**（再解析）で回すこと。

| dockerfile_path      | is_serverless    | 期待                             |
| -------------------- | ---------------- | -------------------------------- |
| `""`                 | –                | 自動生成                         |
| `Dockerfile`         | serverless       | ビルド・起動、中継なし           |
| `variants/port3000`  | serverless / EKS | 中継あり / port 直結             |
| `variants/amd64only` | serverless / EKS | fail-fast / ビルド成功           |
| `variants/alias`     | –                | alias 解決してビルド             |
| `variants/distroless`| serverless       | fail-fast                        |
| `variants/buildkit`  | –                | Kaniko 自然失敗                  |
| `does/not/exist`     | –                | "Dockerfile not found" fail-fast |
