from mini_store.pricing import calculate_order_total


def test_standard_customer_in_mexico_pays_tax_and_shipping():
    assert calculate_order_total(500, "standard", None, "MX") == 679.0


def test_premium_customer_receives_discount():
    assert calculate_order_total(1000, "premium", None, "MX") == 1143.0


def test_save20_coupon_requires_minimum_subtotal():
    assert calculate_order_total(1400, "standard", "SAVE20", "MX") == 1624.0
def test_save5_coupon_applies_discount():
    # 500 - 25 = 475; impuesto = 76; envío = 99.
    assert calculate_order_total(500, "standard", "SAVE5", "MX") == 650.0


def test_save20_coupon_applies_at_minimum_subtotal():
    # 1500 - 300 = 1200; impuesto = 192; envío gratis.
    assert calculate_order_total(1500, "standard", "SAVE20", "MX") == 1392.0


def test_international_order_below_threshold_pays_standard_shipping():
    # Sin impuesto; envío internacional = 299.
    assert calculate_order_total(1999, "standard", None, "US") == 2298.0


def test_international_order_at_threshold_pays_reduced_shipping():
    # Sin impuesto; envío internacional = 199.
    assert calculate_order_total(2000, "standard", None, "US") == 2199.0