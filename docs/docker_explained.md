# Docker & Containerization

## Why Docker?
Docker allows us to package applications with all their dependencies (libraries, runtimes, system tools) into a standardized unit called a **container**.

### Benefits for AI Systems
1.  **Reproducibility**: "It works on my machine" is solved. The `Dockerfile` exactly defines the OS (Linux/Debian), Python version, and libraries.
2.  **Dependency Isolation**: The AI service needs PyTorch and heavy libraries. The API Gateway needs .NET. Docker keeps these environments completely separate, avoiding conflicting versions.
3.  **Efficiency**: We use **Multi-Stage Builds**.
    -   *Builder Stage*: Installs compilers (gcc) and builds dependencies.
    -   *Runtime Stage*: Copies only the artifacts. Result: Much smaller images (e.g., stripping out build tools).

## Key Concepts Used

### Dockerfile
-   `FROM`: Base image.
-   `COPY`: Move code into container.
-   `RUN`: Execute build commands.
-   `CMD`: The process to run when container starts.
-   `HEALTHCHECK`: Critical for orchestration. It tells Docker if the app is actually ready, not just if the process is running.

### Docker Compose
-   Orchestrates multiple containers.
-   Creates a shared virtual network (`ai-network`) so containers can talk to each other by name.
-   Manages volumes and environment variables.
