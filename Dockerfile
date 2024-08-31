FROM python:3.8-bookworm AS builder

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
COPY pyproject.toml poetry.lock ./
RUN poetry install

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.30/supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=9f27ad28c5c57cd133325b2a66bba69ba2235799

RUN curl -fsSLO "$SUPERCRONIC_URL" \
    && echo "${SUPERCRONIC_SHA1SUM}  supercronic-linux-amd64" | sha1sum -c - \
    && chmod +x supercronic-linux-amd64 \
    && mv supercronic-linux-amd64 /usr/local/bin/supercronic

COPY crontab /app/crontab

FROM python:3.8-slim-bookworm

WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .
COPY --from=builder /usr/local/bin/supercronic /usr/local/bin/supercronic

# Install Poetry in the final image
RUN pip install poetry

CMD ["/app/.venv/bin/fastapi", "run", "eksiseyler_api/main.py"]