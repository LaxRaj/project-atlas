# atlas/portfolio.py
import pandas as pd
from dataclasses import dataclass, field
from typing import List

@dataclass
class Holding:
    """Represents a single tax lot of a security."""
    symbol: str
    quantity: float
    cost_basis_per_share: float

    @property
    def market_value(self) -> float:
        # In a real system, this would use a live price feed.
        # For our MVP, we'll fetch this from a mock price source.
        pass # To be implemented

    @property
    def cost_basis(self) -> float:
        return self.quantity * self.cost_basis_per_share

@dataclass
class Portfolio:
    """Represents the user's entire financial state."""
    cash: float
    holdings: List[Holding] = field(default_factory=list)

    def get_total_value(self) -> float:
        """Calculates the total market value of the portfolio."""
        # This will be implemented once we have price data.
        holdings_value = 0 # sum(h.market_value for h in self.holdings)
        return self.cash + holdings_value