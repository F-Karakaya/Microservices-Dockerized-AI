# Multi-stage Dockerfile for AI Service
# Purpose: Optimize image size and security by separating build and runtime stages.

# Stage 1: Builder
# We use a slim Python image to install dependencies.
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies to a user directory
# This allows us to copy only installed packages to the final image
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
# We use a distroless-like or very slim image for production.
# Here we stick to python:3.9-slim for balance between size and debuggability.
FROM python:3.9-slim

WORKDIR /app

# Create a non-root user for security (best practice for K8s)
RUN useradd -m -u 1000 appuser

# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Ensure the local bin is in PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application code
COPY ./app ./app

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Healthcheck to monitor service status
# This is used by Docker Compose and orchestration tools to restart unhealthy containers
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
# We use uvicorn as the ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
