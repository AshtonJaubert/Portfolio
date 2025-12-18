# main.py

import pandas as pd
from surprise import SVD, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split
import joblib
import json
import os

# --- MLOps Artifact Paths ---
DATA_FILE = 'data/ml-100k/Ratings.csv'  # Update this path to your local dataset location
MODEL_FILE = 'models/recommender.pkl'
METRICS_FILE = 'metrics.json'

def prepare_and_train_model():
    """
    1. Loads the ratings data.
    2. Splits data into train/test sets.
    3. Trains an SVD model.
    4. Evaluates the model and saves metrics.
    5. Saves the trained model object.
    """
    print("Starting model training and evaluation...")
    
    # 1. Load Data with correct MovieLens format
    try:
        # Load the raw data (it's tab-separated and has no header)
        ratings_df = pd.read_csv(
            DATA_FILE, 
            sep='\t', 
            header=None,
            names=['userId', 'movieId', 'rating', 'timestamp'],
            encoding='latin-1' # sometimes required for MovieLens
        )
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_FILE}. Please check the path and case.")
        return

    # Use Surprise's Reader class to specify the format of the dataframe
    reader = Reader(rating_scale=(1, 5))
    
    # Load the data from the DataFrame (use the explicitly named columns)
    data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)
    
    # 2. Split data: 80% for training, 20% for testing
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

    # 3. Train Model: SVD (Matrix Factorization)
    print("Training SVD model...")
    algo = SVD(random_state=42)
    algo.fit(trainset)
    
    # 4. Evaluate Model
    predictions = algo.test(testset)
    rmse = accuracy.rmse(predictions, verbose=False)
    mae = accuracy.mae(predictions, verbose=False)

    metrics = {
        'rmse': rmse,
        'mae': mae
    }

    # Save Metrics
    with open(METRICS_FILE, 'w') as f:
        json.dump(metrics, f)
    print(f"Metrics saved to {METRICS_FILE}: {metrics}")

    # 5. Save Trained Model
    # We use joblib because the Surprise library's dump/load is a bit simpler
    # but joblib is standard for scikit-learn based models.
    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
    joblib.dump(algo, MODEL_FILE)
    print(f"Model saved to {MODEL_FILE}")

if __name__ == '__main__':
    # NOTE: You will need to manually download the MovieLens 100K data
    # and rename the ratings file to 'ratings.csv' in the 'data/' folder first.
    prepare_and_train_model()