# Stage 1: Builder
FROM python:3.12-alpine AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install build dependencies required by many Python packages
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into a custom location using uv
RUN uv sync --frozen --no-dev --no-install-project

# Stage 2: Final image
FROM python:3.12-alpine

WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy your application code
COPY . .

# Make sure the venv is used
ENV PATH="/app/.venv/bin:$PATH"

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]