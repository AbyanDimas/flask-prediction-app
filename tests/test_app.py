import pytest
import json
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index_page(client):
    """Test that the index page loads."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'House Price Predictor' in rv.data

def test_health_endpoint(client):
    """Test the health check endpoint."""
    rv = client.get('/api/health')
    assert rv.status_code == 200
    
    data = json.loads(rv.data)
    assert data['status'] == 'healthy'
    assert 'model_loaded' in data
    assert 'timestamp' in data

def test_model_info_endpoint(client):
    """Test the model info endpoint."""
    rv = client.get('/api/model-info')
    assert rv.status_code == 200
    
    data = json.loads(rv.data)
    assert data['model_type'] == 'Random Forest Regressor'
    assert 'features' in data
    assert len(data['features']) == 5

def test_predict_endpoint_valid_data(client):
    """Test prediction with valid data."""
    test_data = {
        'area': 2000,
        'bedrooms': 3,
        'bathrooms': 2,
        'age': 10,
        'location_score': 7.5
    }
    
    rv = client.post('/api/predict', 
                     data=json.dumps(test_data),
                     content_type='application/json')
    
    assert rv.status_code == 200
    
    data = json.loads(rv.data)
    assert data['success'] == True
    assert 'prediction' in data
    assert 'confidence' in data
    assert data['prediction'] > 0

def test_predict_endpoint_invalid_data(client):
    """Test prediction with invalid data."""
    test_data = {
        'area': -1000,  # Invalid negative area
        'bedrooms': 3,
        'bathrooms': 2,
        'age': 10
    }
    
    rv = client.post('/api/predict', 
                     data=json.dumps(test_data),
                     content_type='application/json')
    
    assert rv.status_code == 400
    
    data = json.loads(rv.data)
    assert data['success'] == False
    assert 'errors' in data

def test_predict_endpoint_missing_data(client):
    """Test prediction with missing required data."""
    test_data = {
        'area': 2000,
        # Missing required fields
    }
    
    rv = client.post('/api/predict', 
                     data=json.dumps(test_data),
                     content_type='application/json')
    
    assert rv.status_code == 400
    
    data = json.loads(rv.data)
    assert data['success'] == False
    assert 'errors' in data

