/**
 * Action Recognition Frontend Application
 * Handles image upload, preview, and prediction display
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

// DOM Elements
const imageInput = document.getElementById('imageInput');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const removeImageBtn = document.getElementById('removeImage');
const predictBtn = document.getElementById('predictBtn');
const resultsSection = document.getElementById('resultsSection');
const predictedAction = document.getElementById('predictedAction');
const confidenceScore = document.getElementById('confidenceScore');
const confidenceProgress = document.getElementById('confidenceProgress');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

// State
let selectedFile = null;

/**
 * Initialize event listeners
 */
function init() {
    imageInput.addEventListener('change', handleImageSelect);
    removeImageBtn.addEventListener('change', handleRemoveImage);
    predictBtn.addEventListener('click', handlePredict);
    
    // Also allow removing image by clicking the remove button
    removeImageBtn.addEventListener('click', handleRemoveImage);
}

/**
 * Handle image file selection
 */
function handleImageSelect(event) {
    const file = event.target.files[0];
    
    if (!file) {
        return;
    }
    
    // Validate file type - only JPG/JPEG allowed
    const allowedTypes = ['image/jpeg', 'image/jpg'];
    if (!allowedTypes.includes(file.type.toLowerCase())) {
        showError('Please select a JPG or JPEG image file only');
        return;
    }
    
    // Validate file size
    if (file.size > MAX_FILE_SIZE) {
        showError(`File size exceeds 10MB. Please select a smaller image.`);
        return;
    }
    
    // Store selected file
    selectedFile = file;
    
    // Display preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        imagePreview.classList.remove('hidden');
        predictBtn.classList.remove('hidden');
        predictBtn.disabled = false;
        
        // Hide results and errors
        resultsSection.classList.add('hidden');
        hideError();
    };
    reader.readAsDataURL(file);
}

/**
 * Handle remove image action
 */
function handleRemoveImage() {
    // Reset state
    selectedFile = null;
    imageInput.value = '';
    previewImg.src = '';
    
    // Hide elements
    imagePreview.classList.add('hidden');
    predictBtn.classList.add('hidden');
    resultsSection.classList.add('hidden');
    hideError();
    
    // Reset button
    predictBtn.disabled = true;
}

/**
 * Handle prediction request
 */
async function handlePredict() {
    if (!selectedFile) {
        showError('Please select an image first');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    hideError();
    resultsSection.classList.add('hidden');
    
    try {
        // Create FormData and append image
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        // Send request to backend
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            body: formData
        });
        
        // Check response status
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Server error: ${response.status}`);
        }
        
        // Parse response
        const data = await response.json();
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Prediction error:', error);
        
        // Show user-friendly error message
        if (error.message.includes('Failed to fetch')) {
            showError('Unable to connect to server. Please ensure the backend is running on port 8000.');
        } else {
            showError(error.message || 'An error occurred during prediction. Please try again.');
        }
    } finally {
        setLoadingState(false);
    }
}

/**
 * Display prediction results
 */
function displayResults(data) {
    const { action, confidence } = data;
    
    // Format action name (replace underscores with spaces, capitalize)
    const formattedAction = formatActionName(action);
    
    // Update DOM
    predictedAction.textContent = formattedAction;
    confidenceScore.textContent = `${(confidence * 100).toFixed(2)}%`;
    
    // Update confidence bar
    const confidencePercentage = Math.round(confidence * 100);
    confidenceProgress.style.width = `${confidencePercentage}%`;
    
    // Set color based on confidence level
    if (confidence >= 0.8) {
        confidenceProgress.style.backgroundColor = '#10b981'; // Green
    } else if (confidence >= 0.5) {
        confidenceProgress.style.backgroundColor = '#f59e0b'; // Orange
    } else {
        confidenceProgress.style.backgroundColor = '#ef4444'; // Red
    }
    
    // Show results section with animation
    resultsSection.classList.remove('hidden');
    
    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

/**
 * Format action name for display
 */
function formatActionName(action) {
    return action
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

/**
 * Set loading state
 */
function setLoadingState(isLoading) {
    if (isLoading) {
        loadingSpinner.classList.remove('hidden');
        predictBtn.disabled = true;
        predictBtn.querySelector('.btn-text').textContent = 'Processing...';
    } else {
        loadingSpinner.classList.add('hidden');
        predictBtn.disabled = false;
        predictBtn.querySelector('.btn-text').textContent = 'Predict Action';
    }
}

/**
 * Show error message
 */
function showError(message) {
    errorText.textContent = message;
    errorMessage.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.classList.add('hidden');
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
