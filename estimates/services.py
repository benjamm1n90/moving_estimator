def calculate_price(square_footage, pound_estimate, crew_size):
    hourly_price_per_man = 70  # Base price for the service
    price_per_square_foot = 0.5  # Price per square foot
    price_per_pound = 0.2  # Price per pound

    total_price = ((hourly_price_per_man * crew_size) +
                   (price_per_square_foot * square_footage) +
                   (price_per_pound * pound_estimate) +
                   (hourly_price_per_man * crew_size))
    
    return total_price