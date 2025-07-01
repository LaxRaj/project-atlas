# atlas/data_ingestion.py
import pandas as pd
from typing import List
from atlas.portfolio import Holding, Portfolio

def load_holdings_from_csv(filepath: str) -> List[Holding]:
    """
    Loads holdings from a CSV file, simulating a Plaid API response.
    """
    holdings_df = pd.read_csv(filepath)
    holdings = []
    for _, row in holdings_df.iterrows():
        holdings.append(
            Holding(
                symbol=row['symbol'],
                quantity=row['quantity'],
                cost_basis_per_share=row['cost_basis_per_share']
            )
        )
    return holdings

def create_portfolio_state(holdings_filepath: str, cash_balance: float) -> Portfolio:
    """
    Creates the initial Portfolio object from raw data.
    """
    holdings = load_holdings_from_csv(holdings_filepath)
    return Portfolio(cash=cash_balance, holdings=holdings)