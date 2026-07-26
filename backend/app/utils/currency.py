"""Currency utilities for Zimbabwe multi-currency environment."""
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

# Zimbabwe officially uses ZiG (Zimbabwe Gold) as of 2024
# but USD is widely accepted in healthcare
SUPPORTED_CURRENCIES = {"USD", "ZiG", "ZWL"}

# Default exchange rates (update via admin panel or external API)
# These are placeholders — fetch from RBZ or market rate API in production
DEFAULT_RATES = {
    "USD": Decimal("1.0"),
    "ZiG": Decimal("13.5"),   # Example rate: 1 USD = 13.5 ZiG
    "ZWL": Decimal("1000.0"),   # Legacy ZWL if still in use
}


def to_decimal(value) -> Decimal:
    """Safely convert to Decimal."""
    if value is None:
        return Decimal("0")
    return Decimal(str(value))


def get_exchange_rate(currency_code: str, rates: Optional[dict] = None) -> Decimal:
    """Get exchange rate against base currency (USD)."""
    if currency_code == "USD":
        return Decimal("1.0")
    
    if rates and currency_code in rates:
        return to_decimal(rates[currency_code])
    
    if currency_code in DEFAULT_RATES:
        return DEFAULT_RATES[currency_code]
    
    raise ValueError(f"Unsupported currency: {currency_code}")


def convert_to_base_currency(
    amount,
    currency_code: str,
    exchange_rate: Optional[Decimal] = None,
) -> Decimal:
    """
    Convert amount from given currency to base currency (USD).
    If exchange_rate provided, use it directly (locked at invoice time).
    """
    amt = to_decimal(amount)
    
    if currency_code == "USD":
        return amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    rate = exchange_rate or get_exchange_rate(currency_code)
    base = (amt / rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return base


def convert_from_base_currency(
    amount,
    target_currency: str,
    exchange_rate: Optional[Decimal] = None,
) -> Decimal:
    """Convert from USD to target currency."""
    amt = to_decimal(amount)
    
    if target_currency == "USD":
        return amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    rate = exchange_rate or get_exchange_rate(target_currency)
    converted = (amt * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return converted


def format_currency_zw(amount, currency_code: str = "USD") -> str:
    """Format amount for Zimbabwe display."""
    amt = to_decimal(amount)
    
    if currency_code == "USD":
        return f"${amt:,.2f}"
    elif currency_code == "ZiG":
        return f"ZiG {amt:,.2f}"
    elif currency_code == "ZWL":
        return f"ZWL {amt:,.2f}"
    else:
        return f"{currency_code} {amt:,.2f}"


def format_ecocash_reference(ref: str) -> str:
    """Format Ecocash reference number for display."""
    return ref.strip().upper() if ref else ""


def validate_payment_method_for_currency(method: str, currency: str) -> bool:
    """
    Validate that payment method supports the given currency.
    Example: Ecocash only works with ZiG or USD depending on wallet type.
    """
    method = method.upper()
    currency = currency.upper()
    
    # Cash works with everything
    if method in {"CASH", "USD_CASH", "ZiG_CASH"}:
        return True
    
    # Ecocash typically ZiG-denominated in 2024+
    if method == "ECOCASH":
        return currency in {"ZiG", "ZWL"}
    
    # Zipit/Bank transfer can be either
    if method in {"ZIPIT", "BANK_TRANSFER", "CARD"}:
        return True
    
    # Medical aid claims are usually in USD
    if method == "MEDICAL_AID":
        return currency == "USD"
    
    return True  # Default permissive