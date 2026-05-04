"""
Usage examples demonstrating various ways to use the offer generation system.

Shows:
1. Basic single offer generation
2. Batch processing
3. Custom pricing
4. Error handling
5. API-like usage patterns
"""

import json
from extractor import parse_input
from generator import generate_complete_offer, offer_to_json
from pricing import calculate_final_price


# ============================================================================
# EXAMPLE 1: Basic Single Offer Generation
# ============================================================================

def example_basic_offer():
    """Generate a single offer from user input."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Single Offer Generation")
    print("=" * 70)
    
    # Parse input
    raw_input = "BMW X5 2012 far stanga"
    request = parse_input(raw_input)
    print(f"\nParsed: {request}")
    
    # Generate offer
    offer, offer_text = generate_complete_offer(request)
    
    # Output
    print("\nStructured Offer (JSON):")
    print(offer_to_json(offer))
    
    print("\nHuman-Readable Text:")
    print(offer_text)


# ============================================================================
# EXAMPLE 2: Batch Processing
# ============================================================================

def example_batch_processing():
    """Process multiple offers in batch."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Batch Processing")
    print("=" * 70)
    
    input_requests = [
        "BMW X5 2012 far stanga",
        "Mercedes-Benz C-Class 2015 radiator",
        "Audi A4 2018 far dreapta",
        "Toyota Corolla 2010 oglinda stanga",
    ]
    
    results = []
    
    print("\nProcessing batch...")
    for raw_input in input_requests:
        try:
            request = parse_input(raw_input)
            offer, offer_text = generate_complete_offer(request)
            results.append({
                "input": raw_input,
                "success": True,
                "offer": offer.to_dict(),
                "text": offer_text,
            })
            print(f"  [OK] {raw_input}")
        except Exception as e:
            results.append({
                "input": raw_input,
                "success": False,
                "error": str(e),
            })
            print(f"  [ERROR] {raw_input}: {e}")
    
    # Summary
    successful = sum(1 for r in results if r["success"])
    print(f"\nBatch Results: {successful}/{len(input_requests)} successful")
    
    # Save to JSON
    with open("batch_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Results saved to batch_results.json")
    
    return results


# ============================================================================
# EXAMPLE 3: Custom Pricing Per Part
# ============================================================================

def example_custom_pricing():
    """Generate offers with custom base prices per part."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Custom Pricing Per Part")
    print("=" * 70)
    
    # Custom pricing for specific parts
    custom_prices = {
        "radiator": 450.0,
        "far stanga": 150.0,
        "oglinda stanga": 80.0,
    }
    
    test_cases = [
        ("BMW X5 2012 far stanga", "far stanga"),
        ("Mercedes-Benz C-Class 2015 radiator", "radiator"),
        ("Toyota Corolla 2010 oglinda stanga", "oglinda stanga"),
    ]
    
    print("\nProcessing with custom pricing...")
    for raw_input, part_key in test_cases:
        request = parse_input(raw_input)
        base_price = custom_prices.get(part_key, 200.0)
        
        # Generate offer with custom price
        from generator import create_offer
        offer = create_offer(request, base_price=base_price)
        
        print(f"\n  Input: {raw_input}")
        print(f"  Base Price: {base_price} RON")
        print(f"  Final Price: {offer.pret_cu_tva} RON")


# ============================================================================
# EXAMPLE 4: Error Handling
# ============================================================================

def example_error_handling():
    """Demonstrate robust error handling."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Error Handling")
    print("=" * 70)
    
    invalid_inputs = [
        ("No year in input", "BMW X5 far stanga"),
        ("No brand/model", "2012 far stanga"),
        ("Invalid year (too old)", "BMW X5 1800 far stanga"),
        ("Invalid year (future)", "BMW X5 2200 far stanga"),
        ("Empty input", ""),
    ]
    
    print("\nTesting error handling...")
    for description, raw_input in invalid_inputs:
        try:
            parse_input(raw_input)
            print(f"  [UNEXPECTED] {description}: Parsed successfully")
        except ValueError as e:
            print(f"  [EXPECTED ERROR] {description}")
            print(f"    Error: {e}")


# ============================================================================
# EXAMPLE 5: API-like Response
# ============================================================================

def example_api_response():
    """Generate API-style JSON response."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: API-like Response Format")
    print("=" * 70)
    
    raw_input = "BMW X5 2012 far stanga"
    
    try:
        request = parse_input(raw_input)
        offer, offer_text = generate_complete_offer(request)
        
        # API-style response
        response = {
            "status": "success",
            "timestamp": "2024-05-04T10:30:00Z",
            "data": {
                "offer": offer.to_dict(),
                "text_summary": offer_text,
                "metadata": {
                    "brand": request.brand,
                    "model": request.model,
                    "year": request.year,
                    "part": request.part,
                }
            }
        }
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e),
            "data": None,
        }
    
    print("\nAPI Response:")
    print(json.dumps(response, indent=2, ensure_ascii=False))


# ============================================================================
# EXAMPLE 6: Pricing Analysis
# ============================================================================

def example_pricing_analysis():
    """Analyze pricing for different price points."""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Pricing Analysis")
    print("=" * 70)
    
    test_prices = [100.0, 150.0, 200.0, 300.0, 400.0, 500.0]
    
    print("\nPrice Tier Analysis:")
    print(f"{'Base Price':<15} {'Markup':<12} {'Final Price':<15} {'Tier':<20}")
    print("-" * 60)
    
    for base_price in test_prices:
        metadata = calculate_final_price(base_price)
        
        # Determine tier name
        if base_price <= 150:
            tier = "Low (<=150)"
        elif base_price <= 400:
            tier = "Medium (150-400)"
        else:
            tier = "High (>400)"
        
        print(f"{base_price:<15.2f} {metadata.markup_percentage}%{'':<8} "
              f"{metadata.final_price:<15.2f} {tier:<20}")


# ============================================================================
# MAIN: Run All Examples
# ============================================================================

def run_all_examples():
    """Run all example scenarios."""
    print("\n" + "=" * 70)
    print("AUTOMOTIVE OFFER GENERATION - USAGE EXAMPLES")
    print("=" * 70)
    
    example_basic_offer()
    example_batch_processing()
    example_custom_pricing()
    example_error_handling()
    example_api_response()
    example_pricing_analysis()
    
    print("\n" + "=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    run_all_examples()
