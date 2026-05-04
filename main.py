"""
Main entry point for the automotive offer generation system.

Demonstrates the complete workflow:
1. Parse raw input
2. Extract structured data
3. Apply pricing logic
4. Generate structured offer and text

Example usage:
    python main.py
"""

import sys
from extractor import parse_input
from generator import generate_complete_offer, offer_to_json, offer_to_dict


def process_offer_request(raw_input: str, verbose: bool = True) -> dict:
    """
    Process a single offer request end-to-end.
    
    Args:
        raw_input: Raw input text (e.g., "BMW X5 2012 far stanga")
        verbose: Print detailed output
        
    Returns:
        Dictionary containing parsed request, structured offer, and text
        
    Raises:
        ValueError: If input parsing or processing fails
    """
    try:
        # Step 1: Parse raw input
        if verbose:
            print(f"\n📝 INPUT: {raw_input}")
        
        request = parse_input(raw_input)
        
        if verbose:
            print("\n✓ PARSED REQUEST:")
            print(f"  Brand: {request.brand}")
            print(f"  Model: {request.model}")
            print(f"  Year: {request.year}")
            print(f"  Part: {request.part}")
        
        # Step 2: Generate offer
        offer, offer_text = generate_complete_offer(request)
        
        if verbose:
            print("\n💰 OFFER GENERATED:")
            print(f"  Part: {offer.piesa_ofertata}")
            print(f"  Price: {offer.pret_cu_tva} {offer.moneda}")
            print(f"  Availability: {offer.disponibilitate.value}")
            print(f"  Type: {offer.tip_oferta.value}")
        
        # Step 3: Format output
        offer_json = offer_to_json(offer)
        offer_dict = offer_to_dict(offer)
        
        if verbose:
            print("\n📋 STRUCTURED OUTPUT (JSON):")
            print(offer_json)
            
            print("\n📄 OFFER TEXT:")
            print(offer_text)
        
        return {
            "success": True,
            "input": raw_input,
            "parsed_request": {
                "brand": request.brand,
                "model": request.model,
                "year": request.year,
                "part": request.part,
            },
            "offer_json": offer_json,
            "offer_dict": offer_dict,
            "offer_text": offer_text,
        }
    
    except ValueError as e:
        error_msg = f"❌ Error processing input: {e}"
        if verbose:
            print(error_msg)
        return {
            "success": False,
            "input": raw_input,
            "error": str(e),
        }


def main():
    """Run example offers through the system."""
    
    print("=" * 70)
    print("🚗 AUTOMOTIVE OFFER GENERATION SYSTEM")
    print("=" * 70)
    
    # Example test cases with variations
    test_inputs = [
        "BMW X5 2012 far stanga",  # Main example from requirements
        "mercedes benz c class 2015 radiator",  # Multi-word brand
        "Audi A4 2018 far dreapta",  # Different vehicle
        "toyota corolla 2010 oglinda stanga",  # Another variant
    ]
    
    results = []
    
    for raw_input in test_inputs:
        result = process_offer_request(raw_input, verbose=True)
        results.append(result)
        print("\n" + "-" * 70)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    successful = sum(1 for r in results if r["success"])
    print(f"✓ Successfully processed: {successful}/{len(test_inputs)} requests")
    
    return results


def process_single_input(input_text: str):
    """
    Process a single input from command line.
    
    Usage:
        python main.py "BMW X5 2012 far stanga"
    """
    result = process_offer_request(input_text, verbose=True)
    
    if not result["success"]:
        sys.exit(1)
    
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Process command line argument
        input_text = " ".join(sys.argv[1:])
        result = process_single_input(input_text)
    else:
        # Run demonstration with example inputs
        results = main()
