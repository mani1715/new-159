# ============================================================================
# CURRENCY CONVERTER UTILITY
# ============================================================================
# Fixed exchange rates for currency conversion (Base: INR - Indian Rupee)
# These are approximate rates and should be updated periodically for accuracy
# ============================================================================

# Fixed Exchange Rates (as of 2025)
# All rates are relative to INR (1 INR = X currency)
EXCHANGE_RATES = {
    "INR": 1.00,        # Indian Rupee (Base currency)
    "USD": 0.01198,     # US Dollar (1 INR = 0.01198 USD, or 1 USD = 83.50 INR)
    "EUR": 0.01111,     # Euro (1 INR = 0.01111 EUR, or 1 EUR = 90.00 INR)
    "GBP": 0.00952,     # British Pound (1 INR = 0.00952 GBP, or 1 GBP = 105.00 INR)
    "AED": 0.04396,     # UAE Dirham (1 INR = 0.04396 AED, or 1 AED = 22.75 INR)
    "SGD": 0.01613,     # Singapore Dollar (1 INR = 0.01613 SGD, or 1 SGD = 62.00 INR)
    "AUD": 0.01852,     # Australian Dollar (1 INR = 0.01852 AUD, or 1 AUD = 54.00 INR)
    "CAD": 0.01639,     # Canadian Dollar (1 INR = 0.01639 CAD, or 1 CAD = 61.00 INR)
}

# Currency Symbols for Display
CURRENCY_SYMBOLS = {
    "INR": "₹",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "AED": "د.إ",
    "SGD": "S$",
    "AUD": "A$",
    "CAD": "C$",
}

# Currency Names
CURRENCY_NAMES = {
    "INR": "Indian Rupee",
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "AED": "UAE Dirham",
    "SGD": "Singapore Dollar",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
}

def convert_currency(amount: float, from_currency: str = "INR", to_currency: str = "INR") -> float:
    """
    Convert amount from one currency to another using fixed exchange rates
    
    Args:
        amount: The amount to convert
        from_currency: Source currency code (default: INR)
        to_currency: Target currency code (default: INR)
    
    Returns:
        float: Converted amount rounded to 2 decimal places
    
    Example:
        convert_currency(100000, "INR", "USD")  # Converts ₹100,000 to $1,198.00
    """
    if from_currency not in EXCHANGE_RATES:
        raise ValueError(f"Unknown source currency: {from_currency}")
    
    if to_currency not in EXCHANGE_RATES:
        raise ValueError(f"Unknown target currency: {to_currency}")
    
    # Convert from source currency to INR, then from INR to target currency
    if from_currency == "INR":
        amount_in_inr = amount
    else:
        amount_in_inr = amount / EXCHANGE_RATES[from_currency]
    
    # Convert from INR to target currency
    converted_amount = amount_in_inr * EXCHANGE_RATES[to_currency]
    
    return round(converted_amount, 2)

def format_currency(amount: float, currency: str = "INR") -> str:
    """
    Format amount with currency symbol
    
    Args:
        amount: The amount to format
        currency: Currency code (default: INR)
    
    Returns:
        str: Formatted currency string
    
    Example:
        format_currency(100000, "INR")  # Returns "₹100,000.00"
        format_currency(1198, "USD")    # Returns "$1,198.00"
    """
    symbol = CURRENCY_SYMBOLS.get(currency, currency)
    
    # Format with thousands separator
    formatted_amount = f"{amount:,.2f}"
    
    # Different formats for different currencies
    if currency in ["INR"]:
        # Indian format (₹ before amount)
        return f"{symbol}{formatted_amount}"
    else:
        # International format (symbol before amount)
        return f"{symbol}{formatted_amount}"

def get_all_currencies():
    """
    Get list of all supported currencies with their details
    
    Returns:
        list: List of dicts with currency info
    """
    return [
        {
            "code": code,
            "name": CURRENCY_NAMES[code],
            "symbol": CURRENCY_SYMBOLS[code],
            "rate_from_inr": EXCHANGE_RATES[code]
        }
        for code in EXCHANGE_RATES.keys()
    ]

def get_currency_info(currency: str):
    """
    Get information about a specific currency
    
    Args:
        currency: Currency code
    
    Returns:
        dict: Currency information or None if not found
    """
    if currency not in EXCHANGE_RATES:
        return None
    
    return {
        "code": currency,
        "name": CURRENCY_NAMES[currency],
        "symbol": CURRENCY_SYMBOLS[currency],
        "rate_from_inr": EXCHANGE_RATES[currency]
    }

# ============================================================================
# USAGE EXAMPLES
# ============================================================================
"""
# Convert ₹100,000 to USD
amount_usd = convert_currency(100000, "INR", "USD")  # Returns 1198.00

# Format for display
formatted = format_currency(amount_usd, "USD")  # Returns "$1,198.00"

# Get all currencies
currencies = get_all_currencies()
# Returns: [
#   {"code": "INR", "name": "Indian Rupee", "symbol": "₹", "rate_from_inr": 1.0},
#   {"code": "USD", "name": "US Dollar", "symbol": "$", "rate_from_inr": 0.01198},
#   ...
# ]
"""
