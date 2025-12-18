# app.py

import joblib
from fastapi import FastAPI
from surprise import Prediction # We need the Prediction object for type hinting/checking
import os

# --- Configuration ---
# Path to the model file saved by joblib in main.py
MODEL_PATH = 'models/recommender.pkl'

# Initialize FastAPI app
app = FastAPI(title="MLOps Recommender Service", version="1.0")

# Placeholder for the loaded model
model = None

@app.on_event("startup")
def load_model():
    """Load the trained model when the API starts up."""
    global model
    try:
        if not os.path.exists(MODEL_PATH):
            print(f"ERROR: Model file not found at {MODEL_PATH}. Check if dvc repro ran.")
            return

        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        model = None

@app.get("/")
def health_check():
    """Simple health check endpoint."""
    if model:
        return {"status": "ok", "message": "Recommender API is ready", "model_loaded": True}
    return {"status": "error", "message": "Model not loaded", "model_loaded": False}

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int, item_id: int = 10):
    """
    Endpoint to get a predicted rating for a specific user and item.
    """
    if not model:
        return {"error": "Model not available"}, 500
    
    # In a real system, you would identify unrated items for the user 
    # and iterate through them to find the highest-rated predictions.
    
    try:
        # The Surprise model predicts the rating
        prediction: Prediction = model.predict(uid=user_id, iid=item_id)
        
        return {
            "user_id": user_id,
            "item_id_predicted": item_id,
            "predicted_rating": prediction.est,
            "details": f"The predicted rating user {user_id} would give to item {item_id}"
        }
    except Exception as e:
        return {"error": f"Prediction failed due to an internal server error: {e}"}, 500