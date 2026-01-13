from pydantic import BaseModel
from typing import Optional, List

# Request model for prediction
class PredictionRequest(BaseModel):
    """
    Schema for the prediction request.
    It expects a 'text' field which is the input for the model.
    """
    text: str

# Response model for prediction
class PredictionResponse(BaseModel):
    """
    Schema for the prediction response.
    Returns the original text, the sentiment label, and the confidence score.
    """
    text: str
    sentiment: str
    confidence: float
    model_version: str

# Health check response
class HealthResponse(BaseModel):
    """
    Schema for health check response.
    """
    status: str
    version: str
