"""
Inference Module for Action Recognition
Provides image preprocessing and prediction functionality using the CNN-LSTM model.
"""

import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import json
import os
from pathlib import Path
from typing import Tuple, Dict
import logging

from cnn_lstm_model import CNN_LSTM_Model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionRecognizer:
    """
    Action recognition predictor using CNN-LSTM model.
    Handles model loading, image preprocessing, and inference.
    """
    
    def __init__(
        self,
        model_path: str = None,
        classes_path: str = None,
        device: str = None
    ):
        """
        Initialize the action recognizer.
        
        Args:
            model_path: Path to the trained model weights (.pth file)
            classes_path: Path to the action classes JSON file
            device: Device to run inference on ('cuda', 'cpu', or None for auto-detect)
        """
        # Set default paths relative to this script's directory
        if model_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(script_dir, "cnn_lstm_action_model.pth")
        
        if classes_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            classes_path = os.path.join(script_dir, "action_classes.json")
        
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
        
        # Load action classes
        self.class_labels = self._load_classes(classes_path)
        self.num_classes = len(self.class_labels)
        logger.info(f"Loaded {self.num_classes} action classes")
        
        # Initialize and load model
        self.model = self._load_model(model_path)
        
        # Define image preprocessing pipeline (ImageNet normalization)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
    def _load_classes(self, classes_path: str) -> Dict[int, str]:
        """Load action class labels from JSON file."""
        try:
            with open(classes_path, 'r') as f:
                class_list = json.load(f)
            # Convert list to dict with index as key
            return {i: label for i, label in enumerate(class_list)}
        except Exception as e:
            logger.error(f"Error loading classes: {e}")
            raise
    
    def _load_model(self, model_path: str) -> torch.nn.Module:
        """Load the trained CNN-LSTM model."""
        try:
            # Initialize model architecture
            model = CNN_LSTM_Model(num_classes=self.num_classes)
            
            # Load trained weights
            checkpoint = torch.load(model_path, map_location=self.device)
            model.load_state_dict(checkpoint)
            
            # Set to evaluation mode and move to device
            model.eval()
            model.to(self.device)
            
            logger.info(f"Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def preprocess_image(self, image_path: str) -> torch.Tensor:
        """
        Load and preprocess an image for model inference.
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Preprocessed image tensor ready for model input
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Apply transformations
            image_tensor = self.transform(image)
            
            # Add batch dimension
            image_tensor = image_tensor.unsqueeze(0)
            
            return image_tensor.to(self.device)
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise
    
    def predict(self, image_tensor: torch.Tensor) -> Tuple[str, float]:
        """
        Perform inference on a preprocessed image tensor.
        
        Args:
            image_tensor: Preprocessed image tensor
            
        Returns:
            Tuple of (predicted_class_label, confidence_score)
        """
        try:
            with torch.no_grad():
                # Forward pass
                outputs = self.model(image_tensor)
                
                # Apply softmax to get probabilities
                probabilities = F.softmax(outputs, dim=1)
                
                # Get predicted class and confidence
                confidence, predicted_idx = torch.max(probabilities, 1)
                
                predicted_class = self.class_labels[predicted_idx.item()]
                confidence_score = confidence.item()
                
                logger.info(f"Predicted: {predicted_class} (confidence: {confidence_score:.4f})")
                
                return predicted_class, confidence_score
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise
    
    def predict_image(self, image_path: str) -> Tuple[str, float]:
        """
        Complete prediction pipeline: preprocess and predict.
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Tuple of (predicted_class_label, confidence_score)
        """
        image_tensor = self.preprocess_image(image_path)
        return self.predict(image_tensor)


# Global recognizer instance for efficient reuse
_recognizer_instance = None


def get_recognizer() -> ActionRecognizer:
    """
    Get or create a singleton ActionRecognizer instance.
    This ensures the model is loaded only once.
    """
    global _recognizer_instance
    if _recognizer_instance is None:
        _recognizer_instance = ActionRecognizer()
    return _recognizer_instance


def predict_image(image_path: str) -> Dict[str, any]:
    """
    Convenience function for single image prediction.
    
    Args:
        image_path: Path to the input image
        
    Returns:
        Dictionary with 'action' and 'confidence' keys
    """
    recognizer = get_recognizer()
    action, confidence = recognizer.predict_image(image_path)
    
    return {
        "action": action,
        "confidence": float(confidence)
    }


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        result = predict_image(image_path)
        print(f"Predicted Action: {result['action']}")
        print(f"Confidence: {result['confidence']:.2%}")
    else:
        print("Usage: python inference.py <image_path>")
