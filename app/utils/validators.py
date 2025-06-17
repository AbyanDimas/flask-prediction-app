def validate_prediction_input(data):
    """Validate input data for house price prediction.
    
    Args:
        data (dict): Input data dictionary
        
    Returns:
        tuple: (is_valid, errors)
    """
    errors = []
    
    # Required fields
    required_fields = ['area', 'bedrooms', 'bathrooms', 'age']
    
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"{field.replace('_', ' ').title()} is required")
            continue
        
        try:
            value = float(data[field])
            
            # Field-specific validations
            if field == 'area':
                if value <= 0 or value > 10000:
                    errors.append("Area must be between 1 and 10,000 sq ft")
            elif field == 'bedrooms':
                if value < 0 or value > 10:
                    errors.append("Bedrooms must be between 0 and 10")
            elif field == 'bathrooms':
                if value < 0 or value > 10:
                    errors.append("Bathrooms must be between 0 and 10")
            elif field == 'age':
                if value < 0 or value > 200:
                    errors.append("Age must be between 0 and 200 years")
                    
        except (ValueError, TypeError):
            errors.append(f"{field.replace('_', ' ').title()} must be a valid number")
    
    # Optional location_score validation
    if 'location_score' in data and data['location_score']:
        try:
            location_score = float(data['location_score'])
            if location_score < 1 or location_score > 10:
                errors.append("Location score must be between 1 and 10")
        except (ValueError, TypeError):
            errors.append("Location score must be a valid number")
    
    return len(errors) == 0, errors

