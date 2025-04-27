# syntax=docker/dockerfile:1
FROM python:3.13-slim AS base

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

FROM base AS builder
WORKDIR /app

# Install dependencies in a virtual environment using pip cache
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt,readonly \
    --mount=type=cache,target=/root/.cache/pip \
    python -m venv .venv && \
    .venv/bin/pip install -r requirements.txt

FROM base AS final
WORKDIR /app

# Copy only the necessary files and folders
COPY --link --from=builder /app/.venv /app/.venv
COPY --link app.py model.py requirements.txt ./
COPY --link templates ./templates

# Set environment to use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Expose the Flask default port
EXPOSE 5000

# Switch to non-root user
USER appuser

# Start the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]