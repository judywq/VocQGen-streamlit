# app/Dockerfile

FROM python:3.11-slim-bullseye
COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/

WORKDIR /app

# git is required by unimorph
RUN apt-get update && apt-get install -y \
    git

COPY pyproject.toml uv.lock ./

RUN uv venv --python 3.11
RUN uv sync --frozen --no-install-project

COPY . .

EXPOSE 8501

ENTRYPOINT ["uv", "run", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
