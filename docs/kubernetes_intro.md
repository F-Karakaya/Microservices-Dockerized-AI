# Kubernetes (K8s) Orchestration

While Docker Compose is great for local development, **Kubernetes** is the standard for production orchestration.

## Key Components Implemented

### 1. Deployment (`ai-deployment.yaml`)
-   Manages a set of identical pods (replicas).
-   Ensures if a pod crashes, a new one is started (Self-healing).
-   **Scaling**: We set `replicas: 2` to have two instances of the AI service running for high availability.

### 2. Service
-   Provides a stable IP address and DNS name for a set of pods.
-   **Load Balancing**: Distributes traffic across the 2 replicas of the AI service.

### 3. Ingress (`ingress.yaml`)
-   Exposes HTTP/HTTPS routes from outside the cluster to services within the cluster.
-   Acts as the entry point for external traffic to reach the API Gateway.

### 4. Probes (Liveness & Readiness)
-   **Liveness Probe**: "Is the container running?" If no, K8s restarts it.
-   **Readiness Probe**: "Is the app ready to accept traffic?" (e.g., Model loaded?). If no, K8s stops sending traffic to it until it passes.

## Scaling
-   **Horizontal Pod Autoscaler (HPA)**: (Concept) Automatically adds more pods when CPU usage exceeds a threshold (e.g., 50%).
-   **Resource Limits**: We define `requests` (guaranteed resources) and `limits` (max resources) to prevent one service from starving the node.
