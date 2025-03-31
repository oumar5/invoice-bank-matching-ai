from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Transaction:
    date: datetime
    description: str
    amount: float
    reference: str

@dataclass
class Invoice:
    date: datetime
    vendor_name: str
    amount: float
    invoice_number: str
    image_path: str

@dataclass
class Match:
    transaction: Transaction
    invoice: Invoice
    confidence_score: float
    match_type: str  # 'exact', 'fuzzy', 'manual' 