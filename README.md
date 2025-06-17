# 🏠 House Price Predictor

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![ML](https://img.shields.io/badge/ML-Random_Forest-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Sebuah aplikasi web machine learning yang dibangun dengan **Flask & Docker** untuk memprediksi harga rumah berdasarkan berbagai fitur menggunakan model **Random Forest**.

## ✨ Fitur Utama

- 🎨 **Web App**: Antarmuka pengguna yang modern dan responsif dengan Bootstrap 5
- 🔌 **RESTful API**: Endpoint API lengkap untuk prediksi, health check, dan informasi model
- 🤖 **ML Model**: Model Random Forest Regressor dengan akurasi tinggi
- 🐳 **Dockerized**: Mudah di-deploy menggunakan Docker dan Docker Compose
- 📊 **Real-time Prediction**: Prediksi langsung dengan confidence score
- 🛡️ **Input Validation**: Validasi input yang komprehensif di frontend dan backend
- 📱 **Responsive Design**: Tampilan yang optimal di semua device
- 🧪 **Testing**: Unit tests dengan pytest
- 📈 **Monitoring**: Health check dan monitoring endpoint

## 🛠️ Tech Stack

### Backend
- **Python 3.11+**
- **Flask 2.3.3** - Web framework
- **scikit-learn** - Machine learning library
- **pandas & numpy** - Data processing
- **gunicorn** - WSGI server

### Frontend
- **HTML5 & CSS3**
- **Bootstrap 5** - UI framework
- **JavaScript ES6+** - Interactive features
- **Font Awesome** - Icons

### DevOps
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy (optional)
- **pytest** - Testing framework

## 📋 Requirements

### Untuk Production
- Docker 20.10+
- Docker Compose 2.0+

### Untuk Development
- Python 3.11+
- Flask 2.3.3+
- pip atau conda

## 🚀 Quick Start

### 1️⃣ Clone Repository

```bash
git clone https://github.com/AbyanDimas/flask-prediction-app
cd flask-prediction-app
```

### 2️⃣ Pilih Metode Installation

#### 🐍 Option A: Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run development server
export FLASK_APP=app.py  # Windows: set FLASK_APP=app.py
export FLASK_ENV=development  # Windows: set FLASK_ENV=development
flask run

# Or run directly
python app.py
```

➡️ Akses aplikasi di `http://localhost:5000`

#### 🐳 Option B: Docker (Recommended)

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f
```

➡️ Akses aplikasi di `http://localhost:5000`

#### 🏗️ Option C: Production dengan Docker

```bash
# Production mode dengan Nginx
docker-compose --profile production up --build

# Or dengan environment variables
FLASK_ENV=production SECRET_KEY=your-secret-key docker-compose up --build
```

➡️ Akses aplikasi di `http://localhost:80`

## 📚 Usage Guide

### 🌐 Web Interface

1. **Akses aplikasi** di browser: `http://localhost:5000`
2. **Isi form prediksi** dengan detail rumah:
   - **Area (sq ft)**: Luas rumah dalam kaki persegi (500-10,000)
   - **Bedrooms**: Jumlah kamar tidur (1-6+)
   - **Bathrooms**: Jumlah kamar mandi (1-4+)
   - **Age (years)**: Umur rumah dalam tahun (0-200)
   - **Location Score**: Skor lokasi 1-10 (kualitas lingkungan)
3. **Klik "Predict House Price"** untuk mendapatkan estimasi harga
4. **Lihat hasil** dengan confidence score dan breakdown harga

### 🔌 REST API Endpoints

#### Health Check
```bash
GET /api/health
```
**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-01-15T10:30:00"
}
```

#### Prediksi Harga
```bash
POST /api/predict
Content-Type: application/json
```
**Request Body:**
```json
{
  "area": 2000,
  "bedrooms": 3,
  "bathrooms": 2.5,
  "age": 10,
  "location_score": 7.5
}
```
**Response:**
```json
{
  "success": true,
  "prediction": 485000.50,
  "confidence": 0.85,
  "formatted_price": "$485,001",
  "features_used": {
    "area": 2000,
    "bedrooms": 3,
    "bathrooms": 2.5,
    "age": 10,
    "location_score": 7.5
  }
}
```

#### Informasi Model
```bash
GET /api/model-info
```
**Response:**
```json
{
  "model_type": "Random Forest Regressor",
  "features": ["area", "bedrooms", "bathrooms", "age", "location_score"],
  "version": "1.0.0",
  "last_trained": "2024-01-15T08:00:00"
}
```

### 💻 Contoh Penggunaan API

#### cURL
```bash
# Health check
curl -X GET http://localhost:5000/api/health

# Prediksi harga
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "area": 2500,
    "bedrooms": 4,
    "bathrooms": 3,
    "age": 5,
    "location_score": 8.0
  }'
```

#### Python
```python
import requests
import json

# Prediksi harga rumah
url = "http://localhost:5000/api/predict"
data = {
    "area": 2500,
    "bedrooms": 4,
    "bathrooms": 3,
    "age": 5,
    "location_score": 8.0
}

response = requests.post(url, json=data)
result = response.json()

print(f"Predicted Price: {result['formatted_price']}")
print(f"Confidence: {result['confidence']:.1%}")
```

#### JavaScript
```javascript
// Fetch API
fetch('/api/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    area: 2500,
    bedrooms: 4,
    bathrooms: 3,
    age: 5,
    location_score: 8.0
  })
})
.then(response => response.json())
.then(data => {
  console.log('Predicted Price:', data.formatted_price);
  console.log('Confidence:', (data.confidence * 100).toFixed(1) + '%');
});
```

## ⚙️ Configuration

### Environment Variables

Buat file `.env` untuk konfigurasi development:

```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000

# Security
SECRET_KEY=dev-secret-key-change-in-production

# Application Settings
APP_NAME=House Price Predictor
APP_VERSION=1.0.0
```

### Production Configuration

Untuk production, set environment variables melalui Docker atau system:

```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export SECRET_KEY=your-super-secret-production-key
```

## 🏗️ Architecture

### Project Structure

```
flask-prediction-app/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── routes.py                # API routes dan web routes
│   ├── models/
│   │   ├── __init__.py
│   │   └── predictor.py         # ML model dan training logic
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py        # Input validation functions
│   │   └── helpers.py           # Helper utilities
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Custom CSS styles
│   │   └── js/
│   │       └── main.js          # Frontend JavaScript
│   └── templates/
│       ├── base.html            # Base template
│       ├── index.html           # Home page
│       └── result.html          # Prediction result page
├── tests/
│   ├── __init__.py
│   └── test_app.py              # Unit tests
├── data/                        # Data files (optional)
├── .env                         # Environment variables
├── .dockerignore               # Docker ignore file
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
├── requirements.txt            # Python dependencies
├── app.py                      # Application entry point
└── README.md                   # Documentation
```

### Component Overview

- **Flask App Factory**: Modular Flask application setup
- **ML Model**: Random Forest Regressor dengan synthetic data generation
- **API Layer**: RESTful endpoints untuk prediksi dan monitoring
- **Web Interface**: Bootstrap-based UI dengan JavaScript interactivity
- **Validation**: Comprehensive input validation di frontend dan backend
- **Docker**: Multi-stage build dengan production optimizations

### Data Flow

1. **User Input** → Web form atau API request
2. **Validation** → Input validation dan sanitization
3. **Feature Processing** → Data transformation untuk model
4. **ML Prediction** → Random Forest model inference
5. **Response** → Formatted hasil dengan confidence score

## 🔍 Model Details

### Features Used

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| `area` | float | 500-10,000 | Luas rumah dalam sq ft |
| `bedrooms` | int | 1-10 | Jumlah kamar tidur |
| `bathrooms` | float | 1-10 | Jumlah kamar mandi |
| `age` | int | 0-200 | Umur rumah dalam tahun |
| `location_score` | float | 1-10 | Skor kualitas lokasi |

### Model Performance

- **Algorithm**: Random Forest Regressor
- **Features**: 5 numerical features
- **Training Data**: 1000 synthetic samples
- **Accuracy**: ~85% (pada synthetic data)
- **Response Time**: <100ms average

### Confidence Score

Confidence score dihitung berdasarkan:
- Model R² score
- Feature value reasonableness
- Similarity dengan training data patterns

## Development

### Running Tests

Tests are organized using `pytest`.

```bash
pytest
```

### Code Style

Code should adhere to PEP 8. Use `flake8` and `black` for code style and formatting.

```bash
flake8 app
black app
```

### Building the Model

The application comes with a pre-trained Random Forest model, but you can train a new model using the `HousePricePredictor` class found in `app/models/predictor.py`.

### Contributing

Feel free to submit issues and enhancement requests.

1. Fork the repo.
2. Create a new branch (`git checkout -b feature-branch-name`).
3. Make your changes and commit (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Create a new Pull Request.

## Author

- AI Assistant

## License
 
This project is licensed under the MIT License.

---

**Enjoy using the House Price Predictor App!** 🎉

This app is designed for educational purposes. It demonstrates how to integrate machine learning models into a web application and deploy with Docker. Feel free to tweak and extend its capabilities!

