# Automotive Offer Generation System (Test Implementation)

A clean, modular, Python system for automated offer generation in an automotive parts platform.

## Test Objective

This implementation focuses on:

- **Extracting** structured data from raw input (brand, model, year, part)
- **Applying** pricing logic based on defined rules
- **Generating** output that matches real platform form fields
- **Maintaining** clean, extensible architecture

The system validates core logic and can be easily extended with supplier integrations and automation.
This implementation focuses on validating the workflow before integrating real supplier data.

---

## Overview

Given a raw input request (e.g., "BMW X5 2012 far stanga"), the system:

1. **Extracts** structured data: brand, model, year, part
2. **Applies** pricing logic with tiered markups
3. **Generates** structured JSON output with Romanian field names
4. **Produces** human-readable offer text

### Example

**Input:**
```
BMW X5 2012 far stanga
```

**Output (Structured JSON):**
```json
{
  "piesa_ofertata": "Far Stanga BMW X5 2012",
  "pret_cu_tva": 260.0,
  "moneda": "RON",
  "um": "buc",
  "tip_oferta": "second_hand",
  "disponibilitate": "in_stoc",
  "observatii": ""
}
```

**Output (Text):**
```
Offer for BMW X5 2012 - far stanga:
Price: 260.00 RON
Availability: in stock
Condition: second-hand
```

---

## System Flow

```
Input Text
    ↓
Extractor (parse brand, model, year, part)
    ↓
Pricing Logic (apply markup based on tier)
    ↓
Generator (create structured output)
    ↓
JSON + Text Output
```

---

## Architecture

### Module Structure

```
├── config.py          # Central configuration (pricing, brands, defaults)
├── models.py          # Data structures (dataclasses, enums)
├── extractor.py       # Parse raw input into structured data
├── pricing.py         # Apply pricing rules from config
├── generator.py       # Generate offers and text output
├── api_example.py     # FastAPI REST API endpoints and examples
├── main.py            # Entry point and examples
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Usage

### Run Demo (All Examples)

```bash
python main.py
```

Output includes all test cases with detailed parsing and offer information.

### Process Single Input

```bash
python main.py "BMW X5 2012 far stanga"
```

## Pricing Logic

### Formula

```
final_price = base_price × (1 + markup_percentage / 100)
```

### Example Calculation

**Input:** "BMW X5 2012 far stanga"

1. **Parse Input:**
   - Brand: BMW
   - Model: X5
   - Year: 2012
   - Part: Far Stanga

2. **Apply Pricing:**
   - Base price: 200 RON
   - Falls in tier: 150 < 200 ≤ 400
   - Markup: +30%
   - Final price: 200 × 1.3 = **260 RON**

3. **Generate Output:**
   - Structured JSON with field `pret_cu_tva: 260.0`
   - Human-readable text with price and availability

---

## API (Optional)

Optional FastAPI layer included for future integration:

```bash
# Install
pip install fastapi uvicorn

# Run
uvicorn api_example:app --reload
```

Access interactive docs at: http://localhost:8000/docs

---

### Supplier Integration

```python
# Add to pricing logic:
def calculate_final_price(base_price, supplier_markup=0):
    final_price = base_price * (1 + markup_percentage / 100)
    return final_price * (1 + supplier_markup)
```

---

## Test Examples

The system includes four test cases:

1. **Main example:** `BMW X5 2012 far stanga`
   - Result: 260 RON, second-hand, in stock

2. **Multi-word brand:** `mercedes benz c class 2015 radiator`
   - Brand: Mercedes-Benz
   - Model: C Class
   - Year: 2015
   - Part: Radiator

3. **Different vehicle:** `Audi A4 2018 far dreapta`
   - Result: 260 RON, second-hand, in stock

4. **Another variant:** `toyota corolla 2010 oglinda stanga`
   - Result: 260 RON, second-hand, in stock

Run all with: `python main.py`

---

## Validation

Basic input validation is included (brand, model, year, part).

---
