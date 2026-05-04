"""
Offer generation module for creating structured and text-based offers.

Converts parsed input and pricing into:
1. Structured JSON matching form field names (in Romanian)
2. Human-readable offer text
"""

import json
from typing import Dict, Any
from models import InputRequest, Offer, TipOferta, Disponibilitate
from pricing import calculate_final_price


def generate_offer_description(request: InputRequest) -> str:
    """
    Create a concise description of the offered part.
    
    Example:
        input: InputRequest(brand='Bmw', model='X5', year=2012, part='Far Stanga')
        output: "Far Stanga Bmw X5 2012"
    
    Args:
        request: Parsed input request
        
    Returns:
        Formatted part description
    """
    return f"{request.part} {request.brand} {request.model} {request.year}"


def generate_offer_text(
    request: InputRequest,
    final_price: float,
    tip: TipOferta = TipOferta.SECOND_HAND,
    disponibilitate: Disponibilitate = Disponibilitate.IN_STOC,
) -> str:
    """
    Generate human-readable offer text.
    
    Example output:
        "Offer for BMW X5 2012 - far stanga:
         Price: 260 RON
         Availability: in stock
         Condition: second-hand"
    
    Args:
        request: Parsed input request
        final_price: Final calculated price with markup
        tip: Offer type (new/second_hand)
        disponibilitate: Availability status
        
    Returns:
        Formatted offer text (English)
    """
    availability_text = {
        Disponibilitate.IN_STOC: "in stock",
        Disponibilitate.LA_COMANDA: "to order",
    }
    
    condition_text = {
        TipOferta.NOU: "new",
        TipOferta.SECOND_HAND: "second-hand",
    }
    
    offer_text = f"""Offer for {request.brand} {request.model} {request.year} - {request.part}:
Price: {final_price:.2f} RON
Availability: {availability_text[disponibilitate]}
Condition: {condition_text[tip]}"""
    
    return offer_text


def create_offer(
    request: InputRequest,
    base_price: float = None,
    tip_oferta: TipOferta = TipOferta.SECOND_HAND,
    disponibilitate: Disponibilitate = Disponibilitate.IN_STOC,
    observatii: str = None,
) -> Offer:
    """
    Create a complete Offer object from parsed request and pricing.
    
    This is the main entry point for offer generation.
    
    Args:
        request: Parsed InputRequest with brand, model, year, part
        base_price: Base price for the part (default from config)
        tip_oferta: Type of offer (new or second-hand)
        disponibilitate: Availability status
        observatii: Optional notes/observations in Romanian
        
    Returns:
        Offer object with all fields populated
    """
    pricing_metadata = calculate_final_price(base_price)
    piesa_ofertata = generate_offer_description(request)
    
    offer = Offer(
        piesa_ofertata=piesa_ofertata,
        pret_cu_tva=pricing_metadata.final_price,
        moneda=pricing_metadata.currency,
        um="buc",
        tip_oferta=tip_oferta,
        disponibilitate=disponibilitate,
        observatii=observatii or "",
    )
    
    return offer


def offer_to_json(offer: Offer, indent: int = 2) -> str:
    """
    Convert Offer object to formatted JSON string.
    
    Args:
        offer: Offer object
        indent: JSON indentation level
        
    Returns:
        JSON string representation
    """
    return json.dumps(offer.to_dict(), indent=indent, ensure_ascii=False)


def offer_to_dict(offer: Offer) -> Dict[str, Any]:
    """
    Convert Offer object to dictionary.
    
    Args:
        offer: Offer object
        
    Returns:
        Dictionary representation with Romanian field names
    """
    return offer.to_dict()


def generate_complete_offer(
    request: InputRequest,
    base_price: float = 200.0,
) -> tuple:
    """
    Generate complete offer package: structured offer + text.
    
    Args:
        request: Parsed InputRequest
        base_price: Base price for the part
        
    Returns:
        Tuple of (Offer object, offer_text)
    """
    offer = create_offer(request, base_price=base_price)
    offer_text = generate_offer_text(
        request,
        offer.pret_cu_tva,
        offer.tip_oferta,
        offer.disponibilitate,
    )
    
    return offer, offer_text
