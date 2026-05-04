"""
Comprehensive test suite for the offer generation system.

Run with: python test_system.py
"""

import unittest
from extractor import parse_input, extract_year, extract_brand_and_model, extract_part
from pricing import calculate_final_price, get_markup_percentage
from generator import create_offer, generate_offer_text, offer_to_dict
from models import TipOferta, Disponibilitate


class TestExtraction(unittest.TestCase):
    """Test data extraction functionality."""
    
    def test_extract_year(self):
        """Test year extraction."""
        assert extract_year("BMW X5 2012 far stanga") == 2012
        assert extract_year("Mercedes 2015 radiator") == 2015
        assert extract_year("No year here") is None
    
    def test_extract_brand_and_model_simple(self):
        """Test brand and model extraction."""
        brand, model = extract_brand_and_model("BMW X5 2012 part")
        assert brand == "Bmw"
        assert model == "X5"
    
    def test_extract_brand_and_model_multiword(self):
        """Test multi-word brand extraction."""
        brand, model = extract_brand_and_model("Mercedes-Benz C-Class 2015 part")
        assert brand == "Mercedes-Benz"
        assert model == "C-Class"
    
    def test_extract_part(self):
        """Test part extraction."""
        part = extract_part("BMW X5 2012 far stanga")
        assert part == "Far Stanga"
        
        part = extract_part("Mercedes-Benz C-Class 2015 radiator")
        assert part == "Radiator"
    
    def test_parse_input_valid(self):
        """Test complete input parsing."""
        request = parse_input("BMW X5 2012 far stanga")
        assert request.brand == "Bmw"
        assert request.model == "X5"
        assert request.year == 2012
        assert request.part == "Far Stanga"
    
    def test_parse_input_invalid_no_year(self):
        """Test parsing fails without year."""
        with self.assertRaises(ValueError):
            parse_input("BMW X5 far stanga")
    
    def test_parse_input_invalid_no_brand(self):
        """Test parsing fails without brand."""
        with self.assertRaises(ValueError):
            parse_input("2012 far stanga")


class TestPricing(unittest.TestCase):
    """Test pricing calculation."""
    
    def test_markup_low_price(self):
        """Test 40% markup for price <= 150 RON."""
        markup = get_markup_percentage(100.0)
        assert markup == 40
    
    def test_markup_medium_price(self):
        """Test 30% markup for 150 < price <= 400 RON."""
        markup = get_markup_percentage(200.0)
        assert markup == 30
        
        markup = get_markup_percentage(400.0)
        assert markup == 30
    
    def test_markup_high_price(self):
        """Test 20% markup for price > 400 RON."""
        markup = get_markup_percentage(500.0)
        assert markup == 20
    
    def test_final_price_calculation_200_ron(self):
        """Test final price for 200 RON base."""
        metadata = calculate_final_price(200.0)
        assert metadata.base_price == 200.0
        assert metadata.markup_percentage == 30
        assert metadata.final_price == 260.0
    
    def test_final_price_calculation_100_ron(self):
        """Test final price for 100 RON base (40% markup)."""
        metadata = calculate_final_price(100.0)
        assert metadata.base_price == 100.0
        assert metadata.markup_percentage == 40
        assert metadata.final_price == 140.0
    
    def test_final_price_calculation_500_ron(self):
        """Test final price for 500 RON base (20% markup)."""
        metadata = calculate_final_price(500.0)
        assert metadata.base_price == 500.0
        assert metadata.markup_percentage == 20
        assert metadata.final_price == 600.0


class TestOffer(unittest.TestCase):
    """Test offer generation."""
    
    def test_create_offer_basic(self):
        """Test basic offer creation."""
        request = parse_input("BMW X5 2012 far stanga")
        offer = create_offer(request)
        
        assert offer.piesa_ofertata == "Far Stanga Bmw X5 2012"
        assert offer.pret_cu_tva == 260.0
        assert offer.moneda == "RON"
        assert offer.um == "buc"
        assert offer.tip_oferta == TipOferta.SECOND_HAND
        assert offer.disponibilitate == Disponibilitate.IN_STOC
    
    def test_offer_to_dict(self):
        """Test offer conversion to dictionary."""
        request = parse_input("BMW X5 2012 far stanga")
        offer = create_offer(request)
        offer_dict = offer_to_dict(offer)
        
        assert isinstance(offer_dict, dict)
        assert offer_dict["piesa_ofertata"] == "Far Stanga Bmw X5 2012"
        assert offer_dict["pret_cu_tva"] == 260.0
        assert offer_dict["tip_oferta"] == "second_hand"
        assert offer_dict["disponibilitate"] == "in_stoc"
    
    def test_offer_text_generation(self):
        """Test human-readable offer text."""
        request = parse_input("BMW X5 2012 far stanga")
        offer_text = generate_offer_text(request, 260.0)
        
        # Note: brand is normalized to title case ("Bmw" not "BMW")
        assert "Bmw" in offer_text
        assert "X5" in offer_text
        assert "260.00 RON" in offer_text
        assert "in stock" in offer_text
        assert "second-hand" in offer_text


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_normalized_casing(self):
        """Test that input is normalized to proper case."""
        request = parse_input("bmw x5 2012 far stanga")
        assert request.brand == "Bmw"
        assert request.model == "X5"
        assert request.part == "Far Stanga"
    
    def test_extra_whitespace(self):
        """Test handling of extra whitespace."""
        request = parse_input("  BMW X5  2012  far stanga  ")
        assert request.brand == "Bmw"
        assert request.model == "X5"
    
    def test_invalid_year_too_old(self):
        """Test rejection of unrealistic year."""
        with self.assertRaises(ValueError):
            parse_input("BMW X5 1850 far stanga")
    
    def test_invalid_year_future(self):
        """Test rejection of far-future year."""
        with self.assertRaises(ValueError):
            parse_input("BMW X5 2200 far stanga")
    
    def test_negative_base_price(self):
        """Test rejection of negative base price."""
        with self.assertRaises(ValueError):
            calculate_final_price(-100.0)


def run_quick_test():
    """Run a quick smoke test."""
    print("[TEST] Running quick smoke test...\n")
    
    test_inputs = [
        "BMW X5 2012 far stanga",
        "Mercedes-Benz C-Class 2015 radiator",
        "Audi A4 2018 far dreapta",
        "toyota corolla 2010 oglinda stanga",
    ]
    
    passed = 0
    failed = 0
    
    for input_text in test_inputs:
        try:
            request = parse_input(input_text)
            offer = create_offer(request)
            assert offer.pret_cu_tva == 260.0  # All default base prices = 200, markup = 30%
            print(f"[PASS] {input_text}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {input_text}: {e}")
            failed += 1
    
    print(f"\n[SUMMARY] Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    import sys
    
    # Run quick smoke test first
    if not run_quick_test():
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("[TEST] Running comprehensive unit tests...\n")
    
    # Run full unit tests
    unittest.main(verbosity=2)
