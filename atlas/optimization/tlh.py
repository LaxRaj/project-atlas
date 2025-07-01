# Tax-Loss Harvesting (TLH) Module
# This module is responsible for generating tax-loss harvesting recommendations.
# It is a simple MVP that does not consider all the complexities of tax-loss harvesting.
# It is a starting point for a more sophisticated system.


# atlas/optimization/tlh.py

from typing import Dict, List, Tuple
from atlas.portfolio import Portfolio, Holding

# Mock price feed for the MVP. In a real app, this would be a live API call.
MOCK_PRICES = {
    "VTI": 230.50, # Purchased at $245.20, now at a loss
    "VXUS": 60.00, # Gain
    "BND": 75.00,  # Loss
}

# Define replacement assets to avoid wash sales.
REPLACEMENT_MAP = {
    "VTI": "IVV",
    "IVV": "VOO",
    "VXUS": "IXUS",
    "BND": "AGG",
}

def find_harvestable_losses(portfolio: Portfolio, current_prices: Dict) -> List[Tuple[Holding, float]]:
    """
    Scans the portfolio for holdings with unrealized losses.

    Returns:
        A list of tuples, each containing a holding and its unrealized loss.
    """
    harvestable_lots = []
    for holding in portfolio.holdings:
        current_price = current_prices.get(holding.symbol)
        if not current_price:
            continue

        unrealized_gain_loss = (current_price - holding.cost_basis_per_share) * holding.quantity

        if unrealized_gain_loss < 0:
            # This lot has a loss, it's a candidate for harvesting.
            harvestable_lots.append((holding, unrealized_gain_loss))
    
    # We could add more logic here, e.g., only harvest losses > $X.
    # For the MVP, we'll consider all losses.
    return harvestable_lots

def generate_tlh_recommendations(portfolio: Portfolio, tax_rate: float = 0.15) -> List[Dict]:
    """
    Generates tax-loss harvesting recommendations.
    """
    recommendations = []
    harvestable_lots = find_harvestable_losses(portfolio, MOCK_PRICES)

    for holding, loss_amount in harvestable_lots:
        tax_savings = abs(loss_amount) * tax_rate
        replacement_asset = REPLACEMENT_MAP.get(holding.symbol)

        if not replacement_asset:
            continue # No replacement asset defined, skip.

        # Calculate how many shares of the replacement to buy
        proceeds_from_sale = holding.quantity * MOCK_PRICES[holding.symbol]
        # We need a price for the replacement asset. Let's assume it's close for now.
        # In a real system, you'd fetch the live price of the replacement.
        MOCK_PRICES[replacement_asset] = MOCK_PRICES[holding.symbol] * 1.01 # Simulate slight price difference
        replacement_quantity = proceeds_from_sale / MOCK_PRICES[replacement_asset]

        # SELL Recommendation
        recommendations.append({
            "action": "SELL",
            "symbol": holding.symbol,
            "quantity": holding.quantity,
            "reason": f"Harvest a ${abs(loss_amount):.2f} loss.",
            "estimated_tax_savings": f"${tax_savings:.2f}"
        })

        # BUY Recommendation (Replacement)
        recommendations.append({
            "action": "BUY",
            "symbol": replacement_asset,
            "quantity": round(replacement_quantity, 2),
            "reason": f"Replacement for {holding.symbol} to maintain market exposure."
        })

    return recommendations