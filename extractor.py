"""
Data extraction module for parsing raw automotive part requests.

Handles parsing unstructured input text into structured components:
- Brand (e.g., BMW, Mercedes-Benz)
- Model (e.g., X5, C-Class)
- Year (e.g., 2012)
- Part (e.g., far stanga, radiator)
"""

import re
from typing import Optional, Tuple
from models import InputRequest
import config


def normalize_brand(text: str) -> str:
    """
    Normalize brand name with correct casing.
    
    Rules:
    - Check multi-word brands in config first (e.g., Mercedes-Benz)
    - Short brands (<=4 chars) → uppercase (e.g., BMW, Audi)
    - Otherwise → title case (e.g., Toyota)
    
    Args:
        text: Raw brand text
        
    Returns:
        Normalized brand with correct casing
    """
    text_lower = text.strip().lower()
    
    if text_lower in config.MULTI_WORD_BRANDS:
        return config.MULTI_WORD_BRANDS[text_lower]
    
    words = text_lower.split()
    first_word = words[0] if words else text_lower
    
    if len(first_word) <= 4:
        return first_word.upper()
    
    return first_word.title()


def normalize_text(text: str) -> str:
    """
    Normalize input text by stripping whitespace and converting to proper case.
    
    Args:
        text: Raw input text
        
    Returns:
        Normalized text
    """
    return text.strip().title()


def extract_year(text: str) -> Optional[int]:
    """
    Extract year from text using regex pattern.
    
    Looks for 4-digit numbers between 1900 and 2100.
    
    Args:
        text: Input text containing potential year
        
    Returns:
        Year as integer or None if not found/invalid
    """
    # Match 4-digit number that looks like a year
    match = re.search(r'\b(19|20)\d{2}\b', text)
    if match:
        year = int(match.group(0))
        # Validate reasonable car year
        if 1900 <= year <= 2100:
            return year
    return None


def extract_brand_and_model(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract brand and model from text.
    
    Handles common patterns:
    - "BMW X5" → brand="BMW", model="X5"
    - "Mercedes-Benz C-Class" → brand="Mercedes-Benz", model="C-Class"
    
    Args:
        text: Input text
        
    Returns:
        Tuple of (brand, model) or (None, None) if extraction fails
    """
    text_without_year = re.sub(r'\b\d{4}\b', '', text).strip()
    
    for brand_pattern in config.MULTI_WORD_BRANDS.keys():
        if text_without_year.lower().startswith(brand_pattern):
            remaining = text_without_year[len(brand_pattern):].strip()
            model_match = re.match(r'(\S+)', remaining)
            if model_match:
                return normalize_brand(brand_pattern), normalize_text(model_match.group(1))
    
    words = text_without_year.split()
    if len(words) >= 2:
        brand = words[0]
        model = words[1]
        return normalize_brand(brand), normalize_text(model)
    
    return None, None


def extract_part(text: str) -> Optional[str]:
    """
    Extract the car part from text.
    
    The part is typically the last meaningful words after brand, model, and year.
    
    Args:
        text: Input text
        
    Returns:
        Extracted part or None
    """
    # Remove year
    text_without_year = re.sub(r'\b\d{4}\b', '', text).strip()
    
    # Remove brand and model (first two words typically)
    words = text_without_year.split()
    if len(words) > 2:
        # Everything after brand and model is the part
        part = ' '.join(words[2:])
        return normalize_text(part) if part.strip() else None
    
    return None


def parse_input(raw_input: str) -> InputRequest:
    """
    Parse raw input text into a structured InputRequest object.
    
    Example:
        input: "BMW X5 2012 far stanga"
        output: InputRequest(brand='Bmw', model='X5', year=2012, part='Far Stanga')
    
    Args:
        raw_input: Raw user input text
        
    Returns:
        InputRequest object with validated data
        
    Raises:
        ValueError: If required fields cannot be extracted or are invalid
    """
    # Normalize input
    raw_input = raw_input.strip()
    if not raw_input:
        raise ValueError("Input cannot be empty")
    
    # Extract components
    year = extract_year(raw_input)
    if year is None:
        raise ValueError(f"Could not extract year from input: '{raw_input}'")
    
    brand, model = extract_brand_and_model(raw_input)
    if not brand or not model:
        raise ValueError(f"Could not extract brand and model from input: '{raw_input}'")
    
    part = extract_part(raw_input)
    if not part:
        raise ValueError(f"Could not extract part from input: '{raw_input}'")
    
    # Create and validate InputRequest
    try:
        return InputRequest(brand=brand, model=model, year=year, part=part)
    except ValueError as e:
        raise ValueError(f"Validation failed: {e}")
