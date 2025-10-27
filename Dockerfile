# Multi-stage build for Django DRF project using uv
FROM python:3.14-slim as base

# Install uv
RUN pip install --no-cache-dir uv

# Stage 1: Install dependencies
FROM base AS builder

WORKDIR /app

# Copy dependency files and project
COPY pyproject.toml uv.lock* ./
COPY penpal/ ./penpal/

# Create virtual environment and install dependencies using uv sync
# uv sync creates a .venv and installs all dependencies
# Try with --frozen (requires uv.lock), fallback to regular sync
RUN if [ -f uv.lock ]; then uv sync --frozen; else uv sync; fi

# Stage 2: Runtime
FROM base AS runtime

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy project files
COPY penpal/ ./penpal/

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Set working directory to penpal
WORKDIR /app/penpal

# Run migrations and start server
CMD python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000

