"""
Pricing logic module for automotive part offers.

Implements pricing rules with tiered markups based on config.
"""

from models import PricingMetadata
import config


def get_markup_percentage(price: float) -> int:
    """
    Determine markup percentage based on price tier from config.
    
    Pricing strategy:
    - Lower-priced items get higher markup (more profit margin)
    - Higher-priced items get lower markup (competitive pricing)
    
    Args:
        price: Base price in RON
        
    Returns:
        Markup percentage
    """
    for threshold, markup in config.PRICING_TIERS:
        if price <= threshold:
            return markup
    return 20


def calculate_final_price(base_price: float = None) -> PricingMetadata:
    """
    Calculate final price with markup applied.
    
    Formula: final_price = base_price * (1 + markup_percentage / 100)
    
    Args:
        base_price: Starting price in RON (default from config)
        
    Returns:
        PricingMetadata object containing base price, markup, and final price
        
    Raises:
        ValueError: If base_price is negative or zero
    """
    if base_price is None:
        base_price = config.DEFAULT_BASE_PRICE
    
    if base_price <= 0:
        raise ValueError(f"Base price must be positive, got {base_price}")
    
    markup_percentage = get_markup_percentage(base_price)
    final_price = base_price * (1 + markup_percentage / 100)
    final_price = round(final_price, 2)
    
    return PricingMetadata(
        base_price=base_price,
        markup_percentage=markup_percentage,
        final_price=final_price,
        currency=config.CURRENCY,
    )


def apply_pricing(base_price: float = None) -> float:
    """
    Get final price after markup.
    
    Args:
        base_price: Starting price in RON (default from config)
        
    Returns:
        Final price after markup
    """
    metadata = calculate_final_price(base_price)
    return metadata.final_price
