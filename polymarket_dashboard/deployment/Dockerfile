# Use slim Python
FROM python:3.13-slim

# Install uv CLI from astral-sh
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy pyproject and lock files first (for layer caching)
# COPY pyproject.toml uv.lock README.md /app/

RUN mkdir /app/src

COPY ./src/ /app/src/

# RUN uv sync --frozen

# ENV PATH="/app/.venv/bin:$PATH"

# EXPOSE 8000

# CMD ["uvicorn", "polymarket_dashboard.src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["sh", "-c", "pwd && ls -R && sleep 1000"]
