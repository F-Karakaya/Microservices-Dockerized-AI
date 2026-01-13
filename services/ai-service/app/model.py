import torch
import logging
from transformers import pipeline
from app.schemas import PredictionRequest, PredictionResponse

# Configure logging
logger = logging.getLogger(__name__)

class AIModel:
    """
    AIModel class handles the loading and inference of the machine learning model.
    It currently uses a pre-trained sentiment analysis model from Hugging Face.
    This demonstrates separation of concerns where model logic is isolated from API logic.
    """
    def __init__(self):
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.analyzer = None
        self.device = -1 # CPU by default, change to 0 for GPU if available and properly configured
        self._load_model()

    def _load_model(self):
        """
        Loads the model pipeline.
        Includes error handling to ensure the service doesn't crash silently.
        """
        try:
            logger.info(f"Loading model: {self.model_name}")
            # Initialize the pipeline for sentiment analysis
            # In a real production scenario, you might load a local model file
            self.analyzer = pipeline("sentiment-analysis", model=self.model_name, device=self.device)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise e

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        """
        Performs inference on the input text.
        
        Args:
            request (PredictionRequest): The input data.
            
        Returns:
            PredictionResponse: The result of the inference.
        """
        if not self.analyzer:
            raise RuntimeError("Model is not loaded.")

        try:
            logger.info(f"Processing request for text length: {len(request.text)}")
            
            # Run inference
            result = self.analyzer(request.text)[0]
            
            # Map result to response schema
            return PredictionResponse(
                text=request.text,
                sentiment=result['label'],
                confidence=result['score'],
                model_version=self.model_name
            )
        except Exception as e:
            logger.error(f"Inference error: {str(e)}")
            raise e
