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

# pump_allowed tests
def test_pump_allowed():
    assert pump_allowed(30, 1, False) is True

def test_fleet_pump():
    assert pump_allowed(150, 0, True) is True

def test_too_many_litres():
    assert pump_allowed(70, 1, False) is False

# session_status tests
def test_card_active():
    assert session_status(90, True, False) == "active"

def test_cash_night_warning():
    # cutoff is 30 + 30 = 60, 50 is within 15 of it
    assert session_status(50, False, True) == "warning"

def test_cash_timed_out():
    assert session_status(10, False, False) == "timed_out"
