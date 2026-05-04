#!/usr/bin/env python
"""
Final verification script - End-to-end system demonstration.

Run with: python verify_system.py
"""

from extractor import parse_input
from generator import generate_complete_offer


def main():
    test_cases = [
        'BMW X5 2012 far stanga',
        'Mercedes-Benz C-Class 2015 radiator',
        'Audi A4 2018 far dreapta',
        'Toyota Corolla 2010 oglinda stanga',
    ]
    
    print('=' * 70)
    print('FINAL VERIFICATION - END-TO-END DEMONSTRATION')
    print('=' * 70)
    
    results = []
    
    for i, raw_input in enumerate(test_cases, 1):
        print(f'\n[TEST {i}] Input: {raw_input}')
        
        try:
            # Parse input
            request = parse_input(raw_input)
            print(f'  Parsed: {request.brand} {request.model} {request.year} - {request.part}')
            
            # Generate offer
            offer, text = generate_complete_offer(request)
            offer_dict = offer.to_dict()
            
            # Display results
            print(f'  Price: {offer_dict["pret_cu_tva"]} {offer_dict["moneda"]}')
            print(f'  Part: {offer_dict["piesa_ofertata"]}')
            print(f'  Type: {offer_dict["tip_oferta"]}')
            print(f'  Availability: {offer_dict["disponibilitate"]}')
            print('  Status: SUCCESS')
            
            results.append({'input': raw_input, 'success': True})
            
        except Exception as e:
            print(f'  Error: {e}')
            print('  Status: FAILED')
            results.append({'input': raw_input, 'success': False, 'error': str(e)})
    
    # Summary
    print('\n' + '=' * 70)
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    print(f'VERIFICATION COMPLETE: {successful}/{total} tests passed')
    print('=' * 70)
    
    if successful == total:
        print('\n[SUCCESS] All tests passed! System is ready for production.')
        return 0
    else:
        print(f'\n[FAILED] {total - successful} test(s) failed.')
        return 1


if __name__ == '__main__':
    exit(main())
