import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HousePricePredictor:
    """House price prediction model using Random Forest."""
    
    def __init__(self, model_path='app/models/house_price_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_names = ['area', 'bedrooms', 'bathrooms', 'age', 'location_score']
        self.training_date = None
        self.model_metrics = {}
        
        # Try to load existing model, otherwise train a new one
        if os.path.exists(model_path):
            self.load_model()
        else:
            self.train_model()
    
    def generate_sample_data(self, n_samples=1000):
        """Generate synthetic house data for training."""
        np.random.seed(42)
        
        # Generate features
        area = np.random.normal(2000, 500, n_samples)
        area = np.clip(area, 500, 5000)  # Reasonable area range
        
        bedrooms = np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.1, 0.2, 0.4, 0.2, 0.1])
        bathrooms = np.random.choice([1, 2, 3, 4], n_samples, p=[0.2, 0.4, 0.3, 0.1])
        age = np.random.uniform(0, 50, n_samples)
        location_score = np.random.uniform(1, 10, n_samples)
        
        # Generate target with realistic relationships
        price = (
            area * 150 +  # $150 per sq ft base
            bedrooms * 20000 +  # $20k per bedroom
            bathrooms * 15000 +  # $15k per bathroom
            (50 - age) * 1000 +  # Newer houses worth more
            location_score * 25000 +  # Location premium
            np.random.normal(0, 30000, n_samples)  # Random noise
        )
        
        # Ensure positive prices
        price = np.clip(price, 50000, 2000000)
        
        return pd.DataFrame({
            'area': area,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'age': age,
            'location_score': location_score,
            'price': price
        })
    
    def train_model(self):
        """Train the house price prediction model."""
        logger.info("Training new house price model...")
        
        # Generate training data
        data = self.generate_sample_data()
        X = data[self.feature_names]
        y = data['price']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.model_metrics = {
            'mae': mae,
            'r2': r2,
            'feature_importance': dict(zip(self.feature_names, self.model.feature_importances_))
        }
        
        self.training_date = datetime.now().isoformat()
        
        logger.info(f"Model trained successfully. MAE: {mae:.2f}, R²: {r2:.3f}")
        
        # Save model
        self.save_model()
    
    def save_model(self):
        """Save the trained model and scaler."""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'training_date': self.training_date,
            'metrics': self.model_metrics
        }
        
        joblib.dump(model_data, self.model_path)
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load the trained model and scaler."""
        try:
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.feature_names = model_data.get('feature_names', self.feature_names)
            self.training_date = model_data.get('training_date')
            self.model_metrics = model_data.get('metrics', {})
            
            logger.info(f"Model loaded from {self.model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            logger.info("Training new model...")
            self.train_model()
    
    def predict(self, features):
        """Make a house price prediction.
        
        Args:
            features (dict): Dictionary with keys: area, bedrooms, bathrooms, age, location_score
            
        Returns:
            float: Predicted house price
        """
        if self.model is None or self.scaler is None:
            raise ValueError("Model not loaded or trained")
        
        # Convert features to array
        feature_array = np.array([[features[name] for name in self.feature_names]])
        
        # Scale features
        feature_array_scaled = self.scaler.transform(feature_array)
        
        # Make prediction
        prediction = self.model.predict(feature_array_scaled)[0]
        
        return max(0, prediction)  # Ensure non-negative price
    
    def get_confidence_score(self, features):
        """Get prediction confidence score based on feature similarity to training data."""
        if self.model is None:
            return 0.0
        
        # Simple confidence based on feature ranges and model performance
        confidence = self.model_metrics.get('r2', 0.8)
        
        # Adjust based on feature reasonableness
        if features['area'] < 300 or features['area'] > 6000:
            confidence *= 0.8
        if features['bedrooms'] > 6 or features['bathrooms'] > 5:
            confidence *= 0.8
        if features['age'] > 100:
            confidence *= 0.8
        
        return min(1.0, max(0.0, confidence))
    
    def is_model_loaded(self):
        """Check if model is loaded and ready."""
        return self.model is not None and self.scaler is not None
    
    def get_timestamp(self):
        """Get current timestamp."""
        return datetime.now().isoformat()
    
    def get_training_date(self):
        """Get model training date."""
        return self.training_date
    
    def get_feature_importance(self):
        """Get feature importance scores."""
        return self.model_metrics.get('feature_importance', {})
    
    def get_model_metrics(self):
        """Get model performance metrics."""
        return self.model_metrics

