import pytest
from arbitrage_tool.arbitrage.classes import Arbitrage, ThreeWayArbitrage

def test_american_to_decimal():
    assert Arbitrage.american_to_decimal(150) == 2.5
    assert Arbitrage.american_to_decimal(-150) == 1.67

def test_american_to_implied():
    assert Arbitrage.american_to_implied(150) == 0.4
    assert Arbitrage.american_to_implied(-150) == 0.6

def test_is_arbitrage():
    # Test cases where arbitrage is possible
    assert Arbitrage(150, -125, 500).is_arbitrage() is True
    assert Arbitrage(100, -110, 1000).is_arbitrage() is True
    
    # Test cases where arbitrage is not possible
    assert Arbitrage(100, 100, 500).is_arbitrage() is False
    assert Arbitrage(100, 50, 500).is_arbitrage() is False

def test_unbiased_arbitrage():
    arb = Arbitrage(150, -125, 500)
    assert arb.unbiased_arbitrage() == (250.0, 250.0)
    
    arb = Arbitrage(100, -100, 1000)
    assert arb.unbiased_arbitrage() == (500.0, 500.0)
    
    arb = Arbitrage(100, 100, 1000)
    assert arb.unbiased_arbitrage() is None

def test_biased_arbitrage():
    arb = Arbitrage(150, -125, 500)
    assert arb.biased_arbitrage(0) == (250.0, 250.0)
    assert arb.biased_arbitrage(1) == (250.0, 250.0)
    
    arb = Arbitrage(100, -100, 1000)
    assert arb.biased_arbitrage(0) == (500.0, 500.0)
    assert arb.biased_arbitrage(1) == (500.0, 500.0)
    
    arb = Arbitrage(100, 100, 1000)
    assert arb.biased_arbitrage(0) is None

def test_biased_prob_threshold():
    arb = Arbitrage(150, -125, 500)
    assert arb.biased_prob_threshold() == (1.0, 1.0)
    
    arb = Arbitrage(100, -100, 1000)
    assert arb.biased_prob_threshold() == (1.0, 1.0)
    
    arb = Arbitrage(100, 100, 1000)
    assert arb.biased_prob_threshold() is None

def test_three_way_arbitrage_unbiased():
    three_way = ThreeWayArbitrage(250, 300, 200, 500)
    assert three_way.unbiased_arbitrage() == (166.67, 166.67, 166.67)
    
    three_way = ThreeWayArbitrage(200, 200, 200, 1000)
    assert three_way.unbiased_arbitrage() == (333.33, 333.33, 333.33)
    
    three_way = ThreeWayArbitrage(200, 200, 200, 500)
    assert three_way.unbiased_arbitrage() is None

def test_three_way_arbitrage_biased():
    three_way = ThreeWayArbitrage(250, 300, 200, 500)
    assert three_way.biased_arbitrage(0) == (333.33, 83.33, 83.33)
    assert three_way.biased_arbitrage(1) == (333.33, 83.33, 83.33)
    assert three_way.biased_arbitrage(2) == (333.33, 83.33, 83.33)
    
    three_way = ThreeWayArbitrage(200, 200, 200, 1000)
    assert three_way.biased_arbitrage(0) == (666.67, 166.67, 166.67)
    assert three_way.biased_arbitrage(1) == (666.67, 166.67, 166.67)
    assert three_way.biased_arbitrage(2) == (666.67, 166.67, 166.67)
    
    three_way = ThreeWayArbitrage(200, 200, 200, 500)
    assert three_way.biased_arbitrage(0) is None

# Additional tests can be added as needed.

if __name__ == "__main__":
    pytest.main()
