import pytest
from fuel_station import fuel_bill, pump_allowed, session_status

# fuel_bill tests
def test_within_covered_litres():
    assert fuel_bill("regular", 8, "silver") == 0

def test_unknown_grade():
    with pytest.raises(ValueError):
        fuel_bill("kerosene", 20, "silver")

def test_negative_litres():
    with pytest.raises(ValueError):
        fuel_bill("regular", -5, "silver")

def test_regular_extra_litres():
    # 20 - 10 covered = 10 extra at 105
    assert fuel_bill("regular", 20, "silver") == 1050

def test_diesel_extra_litres():
    # 30 - 20 covered = 10 extra at 90
    assert fuel_bill("diesel", 30, "silver") == 900

def test_premium_gold_bulk():
    # gold gets 5 more so covered = 20, extra = 40
    # rate = 105 - 6 - 4 = 95
    assert fuel_bill("premium", 60, "gold") == 3800

def test_gold_exactly_covered():
    # 10 + 5 bonus = 15 so nothing to pay
    assert fuel_bill("regular", 15, "gold") == 0

def test_gold_diesel_no_bonus():
    # diesel doesnt get the gold bonus, covered stays 20
    assert fuel_bill("diesel", 25, "gold") == 450

def test_bulk_not_gold():
    # extra = 40 so rate drops by 6 only -> 99
    assert fuel_bill("regular", 50, "silver") == 3960

def test_extra_exactly_30():
    # 30 is not > 30 so normal rate
    assert fuel_bill("regular", 40, "silver") == 3150

def test_diesel_bulk_gold():
    # extra = 40, rate = 90 - 6 - 4 = 80
    assert fuel_bill("diesel", 60, "gold") == 3200
