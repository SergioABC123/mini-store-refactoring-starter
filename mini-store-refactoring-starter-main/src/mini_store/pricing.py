"""Pricing rules for orders."""


def calculate_customer_discount(
    subtotal: float,
    customer_type: str,
) -> float:
    rates = {
        "premium": 0.10,
        "employee": 0.15,
    }
    return subtotal * rates.get(customer_type, 0.0)


def calculate_coupon_discount(
    subtotal: float,
    coupon_code: str | None,
) -> float:
    if coupon_code == "SAVE5":
        return subtotal * 0.05

    if coupon_code == "SAVE20" and subtotal >= 1500:
        return subtotal * 0.20

    return 0.0


def calculate_discount(
    subtotal: float,
    customer_type: str,
    coupon_code: str | None,
) -> float:
    customer_discount = calculate_customer_discount(
        subtotal, customer_type
    )
    coupon_discount = calculate_coupon_discount(subtotal, coupon_code)

    return customer_discount + coupon_discount


def calculate_shipping(
    discounted_subtotal: float,
    country: str,
) -> float:
    if country == "MX":
        return 0.0 if discounted_subtotal >= 1000 else 99.0

    return 199.0 if discounted_subtotal >= 2000 else 299.0


def calculate_tax(
    discounted_subtotal: float,
    country: str,
) -> float:
    if country == "MX":
        return discounted_subtotal * 0.16

    return 0.0


def calculate_order_total(
    subtotal: float,
    customer_type: str,
    coupon_code: str | None,
    country: str,
) -> float:
    """Return the final order total after discounts, tax, and shipping."""
    discount = calculate_discount(subtotal, customer_type, coupon_code)
    discounted_subtotal = max(subtotal - discount, 0.0)

    shipping = calculate_shipping(discounted_subtotal, country)
    tax = calculate_tax(discounted_subtotal, country)

    return round(discounted_subtotal + tax + shipping, 2)