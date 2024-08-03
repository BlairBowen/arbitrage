import pytest
from arbitrage_tool.arbitrage.classes import Arbitrage, ThreeWayArbitrage

def test_american_to_decimal():
    assert Arbitrage.american_to_decimal(150) == 2.5
    assert Arbitrage.american_to_decimal(-150) == 1.67

def test_american_to_implied():
    assert Arbitrage.american_to_implied(150) == 0.4
    assert Arbitrage.american_to_implied(-400) == 0.8

def test_is_arbitrage():
    # Test cases where arbitrage is possible
    assert Arbitrage(150, -125, 500).is_arbitrage() is True
    assert Arbitrage(-200, 300, 1000).is_arbitrage() is True
    
    # Test cases where arbitrage is not possible
    assert Arbitrage(100, 100, 500).is_arbitrage() is False
    assert Arbitrage(100, 50, 500).is_arbitrage() is False

def test_unbiased_arbitrage():
    arb = Arbitrage(150, -125, 500)
    assert arb.unbiased_arbitrage() == (209.21, 290.79)
    
    arb = Arbitrage(-200, 300, 1000)
    assert arb.unbiased_arbitrage() == (727.37, 272.63)
    
    arb = Arbitrage(100, 100, 1000)
    assert arb.unbiased_arbitrage() is None

def test_biased_arbitrage():
    arb = Arbitrage(150, -125, 500)
    assert arb.biased_arbitrage(0) == (222.0, 278.0)
    assert arb.biased_arbitrage(1) == (200.0, 300.0)
    
    arb = Arbitrage(-200, 300, 1000)
    assert arb.biased_arbitrage(0) == (750.0, 250.0)
    assert arb.biased_arbitrage(1) == (667.0, 333.0)
    
    arb = Arbitrage(100, 100, 1000)
    assert arb.biased_arbitrage(0) is None

def test_biased_prob_threshold():
    arb = Arbitrage(150, -125, 500)
    assert arb.biased_prob_threshold() == (0.94, 0.97)
    
    arb = Arbitrage(-200, 300, 1000)
    assert arb.biased_prob_threshold() == (0.97, 0.82)
    
    arb = Arbitrage(100, 100, 1000)
    assert arb.biased_prob_threshold() is None

def test_three_way_arbitrage_unbiased():
    three_way = ThreeWayArbitrage(250, 300, 200, 500)
    assert three_way.unbiased_arbitrage() == (164.56, 143.84, 191.6)
    
    three_way = ThreeWayArbitrage(220, 190, 400, 1000)
    assert three_way.unbiased_arbitrage() == (364.06, 402.57, 233.37)
    
    three_way = ThreeWayArbitrage(-200, 200, 200, 500)
    assert three_way.unbiased_arbitrage() is None

def test_three_way_arbitrage_biased():
    three_way = ThreeWayArbitrage(250, 300, 200, 500)
    assert three_way.biased_arbitrage(0) == (208.5, 125.0, 166.5)
    assert three_way.biased_arbitrage(1) == (143.0, 190.5, 166.5)
    assert three_way.biased_arbitrage(2) == (143.0, 125.0, 232.0)
    
    three_way = ThreeWayArbitrage(220, 190, 400, 1000)
    assert three_way.biased_arbitrage(0) == (455.0, 345.0, 200.0)
    assert three_way.biased_arbitrage(1) == (312.0, 488.0, 200.0)
    assert three_way.biased_arbitrage(2) == (312.0, 345.0, 343.0)
    
    three_way = ThreeWayArbitrage(-200, 200, 200, 500)
    assert three_way.biased_arbitrage(0) is None

# Additional tests can be added as needed.

if __name__ == "__main__":
    pytest.main()
