"""
API Integration Example

This module shows how to integrate the offer generation system with a web API.
Uses FastAPI for modern async REST API with automatic Swagger documentation.

To run:
    pip install fastapi uvicorn
    uvicorn api_example:app --reload --port 8000

Then test with:
    curl -X POST http://localhost:8000/api/offers -H "Content-Type: application/json" -d '{"input":"BMW X5 2012 far stanga"}'

API Documentation:
    http://localhost:8000/docs (Swagger UI)
    http://localhost:8000/redoc (ReDoc)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
import json

from extractor import parse_input
from generator import generate_complete_offer


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class OfferRequest(BaseModel):
    """Request model for creating a single offer."""
    input: str
    
    class Config:
        example = {"input": "BMW X5 2012 far stanga"}


class BatchOfferRequest(BaseModel):
    """Request model for creating multiple offers."""
    inputs: List[str]
    
    class Config:
        example = {
            "inputs": [
                "BMW X5 2012 far stanga",
                "Mercedes-Benz C-Class 2015 radiator"
            ]
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Automotive Offer Generation API",
    description="API for generating automotive part offers with pricing",
    version="1.0.0"
)


@app.post("/api/offers")
async def create_offer(request: OfferRequest):
    """
    Create a new offer from raw input.
    
    Args:
        request: OfferRequest with 'input' field (e.g., "BMW X5 2012 far stanga")
        
    Returns:
        JSON response with offer details and parsed components
        
    Raises:
        HTTPException: If input is invalid or processing fails
    """
    if not request.input or not request.input.strip():
        raise HTTPException(status_code=400, detail="Missing or empty 'input' field")
    
    try:
        request_obj = parse_input(request.input)
        offer, offer_text = generate_complete_offer(request_obj)
        
        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "offer": offer.to_dict(),
                "text": offer_text,
                "parsed": {
                    "brand": request_obj.brand,
                    "model": request_obj.model,
                    "year": request_obj.year,
                    "part": request_obj.part,
                }
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/offers/batch")
async def create_offers_batch(request: BatchOfferRequest):
    """
    Create multiple offers in batch.
    
    Args:
        request: BatchOfferRequest with 'inputs' list
        
    Returns:
        JSON response with list of offer results
    """
    if not request.inputs:
        raise HTTPException(status_code=400, detail="'inputs' list cannot be empty")
    
    results = []
    for raw_input in request.inputs:
        try:
            request_obj = parse_input(raw_input)
            offer, offer_text = generate_complete_offer(request_obj)
            results.append({
                "input": raw_input,
                "success": True,
                "offer": offer.to_dict(),
            })
        except Exception as e:
            results.append({
                "input": raw_input,
                "success": False,
                "error": str(e),
            })
    
    return {
        "status": "success",
        "timestamp": datetime.utcnow().isoformat(),
        "results": results
    }


@app.get("/api/health")
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        JSON response indicating service health
    """
    return {
        "status": "healthy",
        "service": "offer-generation-api",
        "version": "1.0.0"
    }


# ============================================================================
# HTTP CLIENT EXAMPLES
# ============================================================================

def example_api_calls():
    """
    Examples of API calls you can make to the FastAPI server.
    
    Run these with curl (or any HTTP client):
    """
    
    examples = {
        "single_offer": {
            "method": "POST",
            "url": "http://localhost:8000/api/offers",
            "headers": {"Content-Type": "application/json"},
            "body": {
                "input": "BMW X5 2012 far stanga"
            },
            "description": "Create a single offer"
        },
        "batch_offers": {
            "method": "POST",
            "url": "http://localhost:8000/api/offers/batch",
            "headers": {"Content-Type": "application/json"},
            "body": {
                "inputs": [
                    "BMW X5 2012 far stanga",
                    "Mercedes-Benz C-Class 2015 radiator",
                    "Audi A4 2018 far dreapta",
                ]
            },
            "description": "Create multiple offers at once"
        },
        "health_check": {
            "method": "GET",
            "url": "http://localhost:8000/api/health",
            "description": "Check if the API is running"
        }
    }
    
    print("\n" + "=" * 70)
    print("API EXAMPLES")
    print("=" * 70)
    
    for name, example in examples.items():
        print(f"\n{name.upper()}:")
        print(f"  Description: {example['description']}")
        print(f"  Method: {example['method']}")
        print(f"  URL: {example['url']}")
        if "headers" in example:
            print(f"  Headers: {json.dumps(example['headers'], indent=4)}")
        if "body" in example:
            print(f"  Body: {json.dumps(example['body'], indent=4)}")


# ============================================================================
# CURL COMMANDS
# ============================================================================

def print_curl_commands():
    """Print ready-to-use curl commands."""
    
    print("\n" + "=" * 70)
    print("CURL COMMANDS (Run these in terminal)")
    print("=" * 70)
    
    commands = [
        ('Single Offer', 
         'curl -X POST http://localhost:8000/api/offers '
         '-H "Content-Type: application/json" '
         '-d \'{"input":"BMW X5 2012 far stanga"}\''),
        
        ('Batch Offers',
         'curl -X POST http://localhost:8000/api/offers/batch '
         '-H "Content-Type: application/json" '
         '-d \'{"inputs":["BMW X5 2012 far stanga","Mercedes 2015 radiator"]}\''),
        
        ('Health Check',
         'curl http://localhost:8000/api/health'),
    ]
    
    for description, curl_cmd in commands:
        print(f"\n{description}:")
        print(f"  {curl_cmd}")


# ============================================================================
# PYTHON CLIENT EXAMPLE
# ============================================================================

def example_python_client():
    """
    Example of how to use the API from a Python client.
    
    Requires: pip install requests
    """
    
    code = '''
# Python client example (requires: pip install requests)

import requests
import json

API_URL = \"http://localhost:8000\"

# Create single offer
response = requests.post(
    f"{API_URL}/api/offers",
    json={"input": "BMW X5 2012 far stanga"},
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    result = response.json()
    offer = result["data"]["offer"]
    print(f"Offer: {offer['piesa_ofertata']}")
    print(f"Price: {offer['pret_cu_tva']} {offer['moneda']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())

# Create batch offers
response = requests.post(
    f"{API_URL}/api/offers/batch",
    json={
        "inputs": [
            "BMW X5 2012 far stanga",
            "Mercedes-Benz C-Class 2015 radiator",
        ]
    },
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    results = response.json()
    for result in results["results"]:
        if result["success"]:
            print(f"[OK] {result['input']}")
        else:
            print(f"[ERROR] {result['input']}: {result['error']}")
    '''
    
    print("\n" + "=" * 70)
    print("PYTHON CLIENT EXAMPLE")
    print("=" * 70)
    print(code)


# ============================================================================
# ASYNC API EXAMPLE (Using asyncio)
# ============================================================================

def example_async_client():
    """
    Example of async API client (for high-volume requests).
    
    Requires: pip install aiohttp
    """
    
    code = '''
# Async Python client example (requires: pip install aiohttp)

import asyncio
import aiohttp

async def create_offer(session, input_text):
    """Create offer asynchronously."""
    async with session.post(
        \"http://localhost:8000/api/offers\",
        json={"input": input_text},
        headers={"Content-Type": "application/json"}
    ) as resp:
        return await resp.json()

async def batch_create_offers(inputs):
    """Create multiple offers concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [create_offer(session, inp) for inp in inputs]
        results = await asyncio.gather(*tasks)
        return results

# Usage
async def main():
    inputs = [
        "BMW X5 2012 far stanga",
        "Mercedes-Benz C-Class 2015 radiator",
        "Audi A4 2018 far dreapta",
    ]
    results = await batch_create_offers(inputs)
    for result in results:
        if result["status"] == "success":
            offer = result["data"]["offer"]
            print(f"[OK] {offer['piesa_ofertata']}")

asyncio.run(main())
    '''
    
    print("\n" + "=" * 70)
    print("ASYNC CLIENT EXAMPLE")
    print("=" * 70)
    print(code)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("AUTOMOTIVE OFFER API - INTEGRATION EXAMPLES")
    print("=" * 70)
    
    # Show examples
    example_api_calls()
    print_curl_commands()
    example_python_client()
    example_async_client()
    
    print("\n" + "=" * 70)
    print("HOW TO RUN THE API SERVER:")
    print("=" * 70)
    print("""
    1. Install FastAPI and Uvicorn:
       pip install fastapi uvicorn
    
    2. Run the server:
       uvicorn api_example:app --reload --port 8000
    
    3. Access the API:
       - Interactive docs: http://localhost:8000/docs
       - Alternative docs: http://localhost:8000/redoc
       - API endpoints: http://localhost:8000/api/*
    
    4. Test with curl commands above
    """)
