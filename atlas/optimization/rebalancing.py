# Rebalancing Module
# This module is responsible for generating rebalancing recommendations.
# It is a simple MVP that does not consider all the complexities of rebalancing.
# It is a starting point for a more sophisticated system.

# atlas/optimization/rebalancing.py
from typing import Dict, List
from atlas.portfolio import Portfolio

# 1. Define Asset Classes for our securities
ASSET_CLASS_MAPPING = {
    'VTI': 'US_STOCKS',
    'IVV': 'US_STOCKS',
    'VOO': 'US_STOCKS',
    'VXUS': 'INTL_STOCKS',
    'IXUS': 'INTL_STOCKS',
    'BND': 'BONDS',
    'AGG': 'BONDS',
}

# 2. Define Target Allocations based on risk tolerance
TARGET_ALLOCATIONS = {
    "Aggressive": {"US_STOCKS": 0.55, "INTL_STOCKS": 0.25, "BONDS": 0.20},
    "Moderate": {"US_STOCKS": 0.40, "INTL_STOCKS": 0.20, "BONDS": 0.40},
}

# Mock prices are needed here too
MOCK_PRICES = {
    "VTI": 230.50,
    "VXUS": 60.00,
    "BND": 75.00
}

def calculate_current_allocation(portfolio: Portfolio, prices: Dict) -> Dict:
    """Calculates the current asset class allocation of the portfolio."""
    allocations = {}
    total_value = portfolio.cash + sum(h.quantity * prices.get(h.symbol, 0) for h in portfolio.holdings)

    if total_value == 0:
        return {}
    
    # Group holdings by asset class
    asset_class_values = {"CASH": portfolio.cash}
    for h in portfolio.holdings:
        asset_class = ASSET_CLASS_MAPPING.get(h.symbol)
        if asset_class:
            value = h.quantity * prices.get(h.symbol, 0)
            asset_class_values[asset_class] = asset_class_values.get(asset_class, 0) + value

    # Calculate percentage allocation
    for asset_class, value in asset_class_values.items():
        allocations[asset_class] = value / total_value

    return allocations


def generate_rebalancing_recommendations(
    portfolio: Portfolio, 
    risk_profile: str, 
    drift_threshold: float = 0.05
) -> List[Dict]:
    """Generates trades to rebalance the portfolio."""
    recommendations = []
    target_allocation = TARGET_ALLOCATIONS.get(risk_profile)
    if not target_allocation:
        return []

    current_allocation = calculate_current_allocation(portfolio, MOCK_PRICES)
    total_value = portfolio.cash + sum(h.quantity * MOCK_PRICES.get(h.symbol, 0) for h in portfolio.holdings)
    
    # Calculate drift and identify which asset classes to buy/sell
    trades_needed = {} # {asset_class: dollar_amount_to_trade}
    for asset_class, target_pct in target_allocation.items():
        current_pct = current_allocation.get(asset_class, 0)
        drift = target_pct - current_pct
        
        if abs(drift) > drift_threshold:
            # We need to rebalance this asset class
            dollar_amount = drift * total_value
            trades_needed[asset_class] = dollar_amount

    # For MVP, we will simplify: Use cash to buy underweight assets.
    # A full implementation would handle selling overweight assets tax-efficiently.
    cash_to_invest = portfolio.cash
    
    for asset_class, amount_to_buy in sorted(trades_needed.items(), key=lambda item: item[1], reverse=True):
        if amount_to_buy > 0 and cash_to_invest > 0:
            # Find a representative symbol for this asset class to buy
            symbol_to_buy = next((s for s, ac in ASSET_CLASS_MAPPING.items() if ac == asset_class), None)
            
            if symbol_to_buy:
                buy_amount = min(amount_to_buy, cash_to_invest)
                quantity = buy_amount / MOCK_PRICES.get(symbol_to_buy, 1) # Avoid division by zero
                recommendations.append({
                    "action": "BUY",
                    "symbol": symbol_to_buy,
                    "quantity": round(quantity, 2),
                    "reason": f"Rebalance to target {target_allocation[asset_class]*100}% in {asset_class}."
                })
                cash_to_invest -= buy_amount
                
    return recommendations