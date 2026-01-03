"""
FastAPI Backend for Action Recognition Web Application
Provides REST API endpoint for image-based action prediction.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import tempfile
import os
from pathlib import Path
from typing import Dict

# Import the inference module
import sys
sys.path.append(str(Path(__file__).parent))
from inference import predict_image, get_recognizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Action Recognition API",
    description="REST API for predicting actions in images using CNN-LSTM model",
    version="1.0.0"
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response model
class PredictionResponse(BaseModel):
    """Response model for prediction endpoint."""
    action: str
    confidence: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "action": "playing_guitar",
                "confidence": 0.9523
            }
        }


@app.on_event("startup")
async def startup_event():
    """
    Initialize the model on application startup.
    This ensures the model is loaded once and reused for all requests.
    """
    try:
        logger.info("Initializing Action Recognition model...")
        recognizer = get_recognizer()
        logger.info("Model initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize model: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Action Recognition API",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Upload an image for action prediction",
            "/health": "GET - Health check endpoint",
            "/docs": "GET - API documentation (Swagger UI)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": get_recognizer() is not None
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_action(file: UploadFile = File(...)) -> Dict[str, any]:
    """
    Predict the action in an uploaded image.
    
    Args:
        file: Uploaded image file (JPEG, PNG, etc.)
        
    Returns:
        JSON response with predicted action and confidence score
        
    Raises:
        HTTPException: If file processing or prediction fails
    """
    temp_file_path = None
    
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Please upload an image."
            )
        
        logger.info(f"Received file: {file.filename} ({file.content_type})")
        
        # Create temporary file to store uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            # Read and write uploaded file content
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
            logger.info(f"Saved uploaded file to: {temp_file_path}")
        
        # Perform prediction
        logger.info("Running inference...")
        result = predict_image(temp_file_path)
        
        logger.info(f"Prediction successful: {result['action']} ({result['confidence']:.4f})")
        
        return JSONResponse(
            status_code=200,
            content={
                "action": result["action"],
                "confidence": round(result["confidence"], 4)
            }
        )
        
    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
        
    except Exception as e:
        # Log and return error response
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
        
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.info(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {temp_file_path}: {e}")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred. Please try again later."
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
