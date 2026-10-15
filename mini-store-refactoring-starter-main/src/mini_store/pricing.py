"""Pricing rules for orders."""

CUSTOMER_DISCOUNT_RATES = {
    "premium": 0.10,
    "employee": 0.15,
}

SAVE5_DISCOUNT_RATE = 0.05
SAVE20_DISCOUNT_RATE = 0.20
SAVE20_MIN_SUBTOTAL = 1500.0

MX_TAX_RATE = 0.16
MX_FREE_SHIPPING_MIN = 1000.0
MX_SHIPPING_COST = 99.0

INTERNATIONAL_REDUCED_SHIPPING_MIN = 2000.0
INTERNATIONAL_REDUCED_SHIPPING_COST = 199.0
INTERNATIONAL_STANDARD_SHIPPING_COST = 299.0


def calculate_customer_discount(
    subtotal: float,
    customer_type: str,
) -> float:
    return subtotal * CUSTOMER_DISCOUNT_RATES.get(customer_type, 0.0)


def calculate_coupon_discount(
    subtotal: float,
    coupon_code: str | None,
) -> float:
    if coupon_code == "SAVE5":
        return subtotal * SAVE5_DISCOUNT_RATE

    if coupon_code == "SAVE20" and subtotal >= SAVE20_MIN_SUBTOTAL:
        return subtotal * SAVE20_DISCOUNT_RATE

    return 0.0


def calculate_discount(
    subtotal: float,
    customer_type: str,
    coupon_code: str | None,
) -> float:
    """Calculate both discounts using the original subtotal."""
    customer_discount = calculate_customer_discount(subtotal, customer_type)
    coupon_discount = calculate_coupon_discount(subtotal, coupon_code)

    return customer_discount + coupon_discount


def calculate_shipping(
    discounted_subtotal: float,
    country: str,
) -> float:
    if country == "MX":
        return (
            0.0
            if discounted_subtotal >= MX_FREE_SHIPPING_MIN
            else MX_SHIPPING_COST
        )

    return (
        INTERNATIONAL_REDUCED_SHIPPING_COST
        if discounted_subtotal >= INTERNATIONAL_REDUCED_SHIPPING_MIN
        else INTERNATIONAL_STANDARD_SHIPPING_COST
    )


def calculate_tax(
    discounted_subtotal: float,
    country: str,
) -> float:
    if country == "MX":
        return discounted_subtotal * MX_TAX_RATE

    return 0.0


def calculate_order_total(
    subtotal: float,
    customer_type: str,
    coupon_code: str | None,
    country: str,
) -> float:
    """Apply discounts, then calculate tax and shipping on the net subtotal."""
    discount = calculate_discount(subtotal, customer_type, coupon_code)
    discounted_subtotal = max(subtotal - discount, 0.0)

    shipping = calculate_shipping(discounted_subtotal, country)
    tax = calculate_tax(discounted_subtotal, country)

    return round(discounted_subtotal + tax + shipping, 2)