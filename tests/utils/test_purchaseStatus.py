from src.utils.purchaseStatus import get_purchase_status


def test_get_purchase_status():
    assert get_purchase_status(True) == "Purchased"
    assert get_purchase_status(False) == "Not Purchased"
