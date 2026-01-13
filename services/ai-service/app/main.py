from fastapi import FastAPI, HTTPException
from app.schemas import PredictionRequest, PredictionResponse, HealthResponse
from app.model import AIModel
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Inference Service",
    description="Microservice for performing AI inference (Sentiment Analysis)",
    version="1.0.0"
)

# Global model instance
model_instance: AIModel = None

@app.on_event("startup")
async def startup_event():
    """
    Event handler for application startup.
    Initializes the AI model to ensure it's ready before accepting requests.
    """
    global model_instance
    try:
        model_instance = AIModel()
    except Exception as e:
        logger.critical(f"Failed to initialize AI model: {e}")
        # In a real scenario, we might want to exit if the model is critical
        pass

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Kubernetes use this to determine if the container is alive and ready.
    """
    if model_instance is None:
         raise HTTPException(status_code=503, detail="Model not initialized")
    return HealthResponse(status="healthy", version="1.0.0")

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Inference endpoint.
    Accepts text and returns sentiment analysis result.
    """
    if model_instance is None:
        raise HTTPException(status_code=503, detail="Service not ready")
    
    try:
        result = model_instance.predict(request)
        return result
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal processing error")

if __name__ == "__main__":
    import uvicorn
    # Read port from environment variable, default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
