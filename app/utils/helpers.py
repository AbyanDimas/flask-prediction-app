def format_currency(amount, currency='USD'):
    """Format a numeric amount as currency.
    
    Args:
        amount (float): The amount to format
        currency (str): Currency code (default: USD)
        
    Returns:
        str: Formatted currency string
    """
    if currency == 'USD':
        return f"${amount:,.2f}"
    elif currency == 'IDR':
        return f"Rp {amount:,.0f}"
    else:
        return f"{amount:,.2f} {currency}"

def calculate_price_per_sqft(price, area):
    """Calculate price per square foot.
    
    Args:
        price (float): Total price
        area (float): Area in square feet
        
    Returns:
        float: Price per square foot
    """
    if area <= 0:
        return 0
    return price / area

def get_price_category(price):
    """Categorize house price into ranges.
    
    Args:
        price (float): House price
        
    Returns:
        str: Price category
    """
    if price < 100000:
        return "Budget"
    elif price < 300000:
        return "Affordable"
    elif price < 600000:
        return "Mid-range"
    elif price < 1000000:
        return "High-end"
    else:
        return "Luxury"

def generate_prediction_summary(features, prediction, confidence):
    """Generate a summary of the prediction.
    
    Args:
        features (dict): Input features
        prediction (float): Predicted price
        confidence (float): Confidence score
        
    Returns:
        dict: Prediction summary
    """
    return {
        'predicted_price': prediction,
        'formatted_price': format_currency(prediction),
        'confidence': confidence,
        'confidence_percentage': f"{confidence * 100:.1f}%",
        'price_category': get_price_category(prediction),
        'price_per_sqft': calculate_price_per_sqft(prediction, features['area']),
        'formatted_price_per_sqft': format_currency(calculate_price_per_sqft(prediction, features['area'])),
        'features': features
    }

