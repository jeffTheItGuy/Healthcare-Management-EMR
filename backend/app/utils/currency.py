"""Currency utilities for multi-currency billing."""
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

# Supported currencies (base = USD)
SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP", "ZAR"}

# Default exchange rates (base = USD).
# Update via admin panel or external API in production.
DEFAULT_RATES = {
    "USD": Decimal("1.0"),
    "EUR": Decimal("0.92"),
    "GBP": Decimal("0.79"),
    "ZAR": Decimal("18.5"),
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
    """Convert amount from given currency to base currency (USD)."""
    amt = to_decimal(amount)
    if currency_code == "USD":
        return amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    rate = exchange_rate or get_exchange_rate(currency_code)
    return (amt / rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


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
    return (amt * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def format_currency(amount, currency_code: str = "USD") -> str:
    """Format amount for display."""
    amt = to_decimal(amount)
    if currency_code == "USD":
        return f"${amt:,.2f}"
    elif currency_code == "EUR":
        return f"€{amt:,.2f}"
    elif currency_code == "GBP":
        return f"£{amt:,.2f}"
    return f"{currency_code} {amt:,.2f}"


def format_payment_reference(ref: str) -> str:
    """Normalize a payment reference for display."""
    return ref.strip().upper() if ref else ""


def validate_payment_method_for_currency(method: str, currency: str) -> bool:
    """Validate that a payment method supports the given currency."""
    method = method.upper()
    currency = currency.upper()
    if not currency:
        return False
    allowed = {
        "CASH", "CARD", "BANK_TRANSFER",
        "MOBILE_MONEY", "INSURANCE", "MEDICAL_AID",
    }
    return method in allowed
