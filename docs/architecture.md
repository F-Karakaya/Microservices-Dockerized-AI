# Microservices Architecture

## Overview
This project moves away from the traditional monolithic architecture to a distribute microservices architecture.  
In a monolith, all components (UI, Business Logic, Data Access) reside in a single codebase and deploy as a single unit or executable. While simple initially, it becomes a bottleneck for scaling, reliability, and team velocity.

## Why Microservices?

1.  **Scalability**: We can scale the `ai-service` independently from the `api-gateway`. If inference demand spikes, we only need more AI containers, not more API or UI containers.
2.  **Technology Diversity**: The AI service uses Python (standard for ML), while the Gateway uses C#/.NET (excellent for high-throughput I/O), and the Frontend can use whatever fits the user experience best.
3.  **Isolation**: If the `ai-service` crashes due to a memory leak in the model, the `api-gateway` remains up and can return a graceful "Service Unavailable" error (via Circuit Breaker) instead of taking down the entire system.
4.  **Resilience**: The API Gateway implements the **Circuit Breaker** pattern (using Polly). If the AI service is overwhelmed, the gateway stops creating new requests for a while, giving the AI service time to recover.

## Service Communication

-   **Frontend -> Gateway**: Determine via HTTP/REST. The frontend does not know about the AI service directly. It only talks to the Gateway.
-   **Gateway -> AI Service**: The Gateway acts as a reverse proxy. It routes `/inference` requests to the AI service's `/predict` endpoint.
-   **Docker Networking**: Services communicate using internal DNS names provided by Docker (`http://ai-service:8000`).

## Diagram

(See `outputs/service_flow.png` for a visual representation generated during execution)

`Frontend (UI)` --HTTP--> `API Gateway` --HTTP--> `AI Service (Model)`
