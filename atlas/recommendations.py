# Recommendation Module
# This module is responsible for generating recommendations based on the portfolio and risk profile.
# It is a simple MVP that does not consider all the complexities of recommendations.
# It is a starting point for a more sophisticated system.

# atlas/recommendations.py
from atlas.portfolio import Portfolio
from atlas.optimization.tlh import generate_tlh_recommendations
from atlas.optimization.rebalancing import generate_rebalancing_recommendations

def generate_recommendations(portfolio: Portfolio, risk_profile: str, tax_rate: float = 0.15):
    """
    Runs all optimization modules and synthesizes recommendations.
    """
    # In the MVP, we run them sequentially.
    # A more advanced version would have a conflict resolution layer.
    
    tlh_recs = generate_tlh_recommendations(portfolio, tax_rate)
    rebalancing_recs = generate_rebalancing_recommendations(portfolio, risk_profile)
    
    # Combine and return
    return tlh_recs + rebalancing_recs