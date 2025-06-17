from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.models.predictor import HousePricePredictor
from app.utils.validators import validate_prediction_input
from app.utils.helpers import format_currency
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
main_bp = Blueprint('main', __name__)

# Initialize predictor
predictor = HousePricePredictor()

@main_bp.route('/')
def index():
    """Home page with prediction form."""
    return render_template('index.html')

@main_bp.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    try:
        # Get form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            
        # Validate input
        is_valid, errors = validate_prediction_input(data)
        if not is_valid:
            if request.is_json:
                return jsonify({
                    'success': False,
                    'errors': errors
                }), 400
            else:
                for error in errors:
                    flash(error, 'error')
                return redirect(url_for('main.index'))
        
        # Convert data types
        features = {
            'area': float(data['area']),
            'bedrooms': int(data['bedrooms']),
            'bathrooms': int(data['bathrooms']),
            'age': int(data['age']),
            'location_score': float(data.get('location_score', 5.0))
        }
        
        # Make prediction
        prediction = predictor.predict(features)
        confidence = predictor.get_confidence_score(features)
        
        logger.info(f"Prediction made: {prediction} with confidence: {confidence}")
        
        if request.is_json:
            return jsonify({
                'success': True,
                'prediction': prediction,
                'confidence': confidence,
                'formatted_price': format_currency(prediction),
                'features_used': features
            })
        else:
            flash(f'Predicted price: {format_currency(prediction)} (Confidence: {confidence:.1%})', 'success')
            return render_template('result.html', 
                                 prediction=prediction,
                                 confidence=confidence,
                                 formatted_price=format_currency(prediction),
                                 features=features)
            
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        if request.is_json:
            return jsonify({
                'success': False,
                'error': 'An error occurred during prediction'
            }), 500
        else:
            flash('An error occurred during prediction. Please try again.', 'error')
            return redirect(url_for('main.index'))

@main_bp.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions."""
    return predict()

@main_bp.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor.is_model_loaded(),
        'timestamp': predictor.get_timestamp()
    })

@main_bp.route('/api/model-info')
def model_info():
    """Get model information."""
    return jsonify({
        'model_type': 'Random Forest Regressor',
        'features': ['area', 'bedrooms', 'bathrooms', 'age', 'location_score'],
        'version': '1.0.0',
        'last_trained': predictor.get_training_date()
    })

@main_bp.errorhandler(404)
def not_found_error(error):
    if request.is_json:
        return jsonify({'error': 'Not found'}), 404
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    if request.is_json:
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('errors/500.html'), 500

