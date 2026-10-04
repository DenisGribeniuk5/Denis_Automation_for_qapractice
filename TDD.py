# Create function which calculate discount and it can't be negative


def test_calculate_discount():
    assert calculate_discount(100, 10) == 90
    assert calculate_discount(-100, 20) == 0


def calculate_discount(price, discount):
    if price < 0:
        return 0
    return price - discount
