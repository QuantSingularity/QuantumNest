# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install OS build deps (needed for psycopg2, cryptography, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps into a prefix so we can copy just them
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/install --no-cache-dir -r requirements.txt


# ── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# Runtime OS libs only (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Non-root user for security
RUN useradd --no-create-home --shell /bin/false appuser

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY . .

# Create necessary runtime directories
RUN mkdir -p /app/uploads /app/models /app/logs \
 && chown -R appuser:appuser /app

USER appuser

# Health-check (FastAPI /health endpoint)
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

EXPOSE ${PORT:-8000}

# Default: run with Gunicorn + Uvicorn workers for production
CMD ["sh", "-c", \
     "gunicorn app.main:app \
        --bind 0.0.0.0:${PORT:-8000} \
        --workers ${WORKERS:-2} \
        --worker-class uvicorn.workers.UvicornWorker \
        --timeout 120 \
        --keep-alive 5 \
        --access-logfile - \
        --error-logfile -"]
