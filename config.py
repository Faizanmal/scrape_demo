"""
Configuration module for the automotive offer generation system.

Centralized settings for pricing, defaults, and system behavior.
Easy to customize for different business requirements.
"""


# ============================================================================
# PRICING CONFIGURATION
# ============================================================================

# Default base price for all parts (in RON)
DEFAULT_BASE_PRICE = 200.0

# Currency code
CURRENCY = "RON"

# Unit of measure for all parts
DEFAULT_UNIT = "buc"  # piece

# Pricing tier thresholds and corresponding markups
# Applied based on base price
PRICING_TIERS = [
    (150, 40),      # price <= 150 RON → +40% markup
    (400, 30),      # 150 < price <= 400 RON → +30% markup
    (float('inf'), 20),  # price > 400 RON → +20% markup
]

# ============================================================================
# OFFER DEFAULTS
# ============================================================================

# Default offer type (new or second_hand)
DEFAULT_OFFER_TYPE = "second_hand"

# Default availability status (in_stoc or la_comanda)
DEFAULT_AVAILABILITY = "in_stoc"

# Default observation/notes text
DEFAULT_NOTES = None

# ============================================================================
# BRAND MAPPINGS
# ============================================================================

# Multi-word brands that should be recognized as single units
# Format: lowercase pattern → display name
MULTI_WORD_BRANDS = {
    'mercedes-benz': 'Mercedes-Benz',
    'mercedes benz': 'Mercedes-Benz',
    'range rover': 'Range Rover',
    'land rover': 'Land Rover',
    'rolls royce': 'Rolls Royce',
    'aston martin': 'Aston Martin',
    'alfa romeo': 'Alfa Romeo',
    'bmw i': 'Bmw I',
}

# ============================================================================
# PART-SPECIFIC PRICING (Optional)
# ============================================================================

# Define custom base prices for specific parts
# If a part is not found here, DEFAULT_BASE_PRICE is used
PART_BASE_PRICES = {
    # Examples (uncomment to use):
    # "radiator": 450.0,
    # "far stanga": 180.0,
    # "oglinda": 100.0,
}

# ============================================================================
# VALIDATION CONFIGURATION
# ============================================================================

# Acceptable year range for vehicles
MIN_YEAR = 1900
MAX_YEAR = 2100

# ============================================================================
# TEXT TEMPLATES
# ============================================================================

# Offer text templates for customization
AVAILABILITY_TEXT_EN = {
    "in_stoc": "in stock",
    "la_comanda": "to order",
}

CONDITION_TEXT_EN = {
    "nou": "new",
    "second_hand": "second-hand",
}

OFFER_TEXT_TEMPLATE_EN = """{brand} {model} {year} - {part}:
Price: {price:.2f} {currency}
Availability: {availability}
Condition: {condition}"""

# ============================================================================
# SUPPLIER CONFIGURATION (For future expansion)
# ============================================================================

# Define supplier pricing adjustments
SUPPLIERS = {
    # Example:
    # "supplier_a": {
    #     "markup_adjustment": 0.05,  # +5% on top of standard markup
    #     "availability_discount": -0.10,  # 10% off if items in stock
    # },
}

# ============================================================================
# LOGGING AND DEBUG
# ============================================================================

# Enable detailed logging
DEBUG_MODE = False

# Log file path (if empty, logs to console only)
LOG_FILE = None

# ============================================================================
# API/INTEGRATION SETTINGS
# ============================================================================

# API endpoint (for future dashboard/external integration)
API_BASE_URL = "http://localhost:8000"

# Enable API mode
ENABLE_API = False

# Database connection string (for future persistence)
DATABASE_URL = None


def get_markup_for_price(base_price: float) -> int:
    """
    Get markup percentage based on configured pricing tiers.
    
    Args:
        base_price: Price in RON
        
    Returns:
        Markup percentage
    """
    for threshold, markup in PRICING_TIERS:
        if base_price <= threshold:
            return markup
    # Fallback (should not reach here)
    return PRICING_TIERS[-1][1]


def get_base_price_for_part(part_name: str) -> float:
    """
    Get base price for a specific part, or default.
    
    Args:
        part_name: Name of the part
        
    Returns:
        Base price in RON
    """
    normalized = part_name.lower().strip()
    return PART_BASE_PRICES.get(normalized, DEFAULT_BASE_PRICE)


def get_brand_display_name(brand: str) -> str:
    """
    Get display name for a brand (handles multi-word brands).
    
    Args:
        brand: Brand name (may be multi-word)
        
    Returns:
        Display name with proper formatting
    """
    normalized = brand.lower()
    return MULTI_WORD_BRANDS.get(normalized, brand)
