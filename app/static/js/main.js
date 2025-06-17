// Main JavaScript for House Price Predictor

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });

    // Initialize tooltips if Bootstrap tooltips are available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Initialize form validation
    initializeFormValidation();

    // Initialize API functions
    initializeAPIFunctions();
}

function initializeFormValidation() {
    const form = document.getElementById('predictionForm');
    if (!form) return;

    // Real-time validation
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });

        input.addEventListener('input', function() {
            clearFieldError(this);
        });
    });

    // Form submission
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            return false;
        }
        
        // Show loading state
        showLoadingState();
    });
}

function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let errorMessage = '';

    // Clear previous errors
    clearFieldError(field);

    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = `${getFieldLabel(fieldName)} is required`;
    }

    // Field-specific validation
    if (value && isValid) {
        switch (fieldName) {
            case 'area':
                const area = parseFloat(value);
                if (area <= 0 || area > 10000) {
                    isValid = false;
                    errorMessage = 'Area must be between 1 and 10,000 sq ft';
                }
                break;

            case 'bedrooms':
                const bedrooms = parseInt(value);
                if (bedrooms < 0 || bedrooms > 10) {
                    isValid = false;
                    errorMessage = 'Bedrooms must be between 0 and 10';
                }
                break;

            case 'bathrooms':
                const bathrooms = parseFloat(value);
                if (bathrooms < 0 || bathrooms > 10) {
                    isValid = false;
                    errorMessage = 'Bathrooms must be between 0 and 10';
                }
                break;

            case 'age':
                const age = parseInt(value);
                if (age < 0 || age > 200) {
                    isValid = false;
                    errorMessage = 'Age must be between 0 and 200 years';
                }
                break;

            case 'location_score':
                const score = parseFloat(value);
                if (score < 1 || score > 10) {
                    isValid = false;
                    errorMessage = 'Location score must be between 1 and 10';
                }
                break;
        }
    }

    if (!isValid) {
        showFieldError(field, errorMessage);
    }

    return isValid;
}

function validateForm() {
    const form = document.getElementById('predictionForm');
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });

    return isValid;
}

function showFieldError(field, message) {
    field.classList.add('is-invalid');
    
    // Remove existing error message
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }

    // Add new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function getFieldLabel(fieldName) {
    const labels = {
        'area': 'Area',
        'bedrooms': 'Bedrooms',
        'bathrooms': 'Bathrooms',
        'age': 'Age',
        'location_score': 'Location Score'
    };
    return labels[fieldName] || fieldName;
}

function showLoadingState() {
    const btn = document.getElementById('predictBtn');
    if (btn) {
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Predicting...';
        btn.disabled = true;
    }
}

function initializeAPIFunctions() {
    // API prediction function
    window.predictAPI = async function(data) {
        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Prediction failed');
            }

            return result;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    };

    // Health check function
    window.checkHealth = async function() {
        try {
            const response = await fetch('/api/health');
            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Health check failed:', error);
            return { status: 'error', error: error.message };
        }
    };
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-US').format(number);
}

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.classList.add('fade');
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 150);
            }
        }, 5000);
    });
});

// Sample prediction examples
function fillSampleData(type) {
    const sampleData = {
        starter: {
            area: 1200,
            bedrooms: 2,
            bathrooms: 2,
            age: 15,
            location_score: 6
        },
        family: {
            area: 2500,
            bedrooms: 4,
            bathrooms: 3,
            age: 8,
            location_score: 7
        },
        luxury: {
            area: 4000,
            bedrooms: 5,
            bathrooms: 4,
            age: 3,
            location_score: 9
        }
    };

    const data = sampleData[type];
    if (data) {
        Object.keys(data).forEach(key => {
            const field = document.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = data[key];
                if (key === 'location_score') {
                    const scoreDisplay = document.getElementById('scoreValue');
                    if (scoreDisplay) {
                        scoreDisplay.textContent = data[key];
                    }
                }
            }
        });
    }
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateField,
        validateForm,
        formatCurrency,
        formatNumber
    };
}

