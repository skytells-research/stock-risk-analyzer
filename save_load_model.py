import joblib
import os

# Create a 'models' directory if it doesn't exist
os.makedirs('models', exist_ok=True)

def save_model(model, filename='risk_model.pkl'):
    """
    Save the trained model to disk in the models directory.
    """
    filepath = os.path.join('models', filename)
    joblib.dump(model, filepath)

def load_model(filename='risk_model.pkl'):
    """
    Load a trained model from the models directory.
    """
    filepath = os.path.join('models', filename)
    return joblib.load(filepath)
