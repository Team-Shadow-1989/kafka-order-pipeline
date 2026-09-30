def test_order_has_required_fields():
    order = {
        "order_id": 101,
        "product": "Laptop",
        "amount": 55000
    }

    assert "order_id" in order
    assert "product" in order
    assert "amount" in order


def test_order_id_is_integer():
    order_id = 101
    assert isinstance(order_id, int)


def test_product_is_string():
    product = "Laptop"
    assert isinstance(product, str)


def test_amount_is_positive():
    amount = 55000
    assert amount > 0