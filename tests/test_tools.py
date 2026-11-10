from goldwise.agent.tools import latest_market_rates, market_price_history

def test_tools_are_defined():
    assert latest_market_rates.name == "latest_market_rates"
    assert market_price_history.name == "market_price_history"
