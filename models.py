"""
Data models for the automotive offer generation system.

Defines core data structures using dataclasses for type safety and clarity.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class TipOferta(str, Enum):
    """Type of offer: new or second-hand."""
    NOU = "nou"
    SECOND_HAND = "second_hand"


class Disponibilitate(str, Enum):
    """Product availability status."""
    IN_STOC = "in_stoc"
    LA_COMANDA = "la_comanda"


@dataclass
class InputRequest:
    """Represents the parsed input request from user."""
    brand: str
    model: str
    year: int
    part: str
    
    def __post_init__(self):
        """Validate input data after initialization."""
        if not self.brand or not self.brand.strip():
            raise ValueError("Brand cannot be empty")
        if not self.model or not self.model.strip():
            raise ValueError("Model cannot be empty")
        if self.year < 1900 or self.year > 2100:
            raise ValueError(f"Year {self.year} is invalid. Must be between 1900 and 2100")
        if not self.part or not self.part.strip():
            raise ValueError("Part cannot be empty")
    
    def __str__(self) -> str:
        """Return readable string representation."""
        return f"{self.brand} {self.model} {self.year} - {self.part}"


@dataclass
class Offer:
    """
    Represents a structured offer with Romanian field names.
    This matches the actual form fields from the automotive platform.
    """
    piesa_ofertata: str
    pret_cu_tva: float
    moneda: str = "RON"
    um: str = "buc"
    tip_oferta: TipOferta = TipOferta.SECOND_HAND
    disponibilitate: Disponibilitate = Disponibilitate.IN_STOC
    observatii: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert offer to dictionary for JSON serialization."""
        return {
            "piesa_ofertata": self.piesa_ofertata,
            "pret_cu_tva": self.pret_cu_tva,
            "moneda": self.moneda,
            "um": self.um,
            "tip_oferta": self.tip_oferta.value,
            "disponibilitate": self.disponibilitate.value,
            "observatii": self.observatii,
        }


@dataclass
class PricingMetadata:
    """Holds intermediate pricing calculation data for transparency."""
    base_price: float
    markup_percentage: int
    final_price: float
    currency: str = "RON"
