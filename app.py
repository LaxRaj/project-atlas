# app.py
import streamlit as st
import pandas as pd
from atlas.data_ingestion import create_portfolio_state
from atlas.recommendations import generate_recommendations

st.set_page_config(layout="wide")

st.title("Project Atlas MVP 🚀")
st.write("A recommendation engine to maximize after-tax returns through tax-loss harvesting and goal-based rebalancing.")

# --- Sidebar for User Inputs ---
st.sidebar.header("User Inputs")
risk_profile = st.sidebar.selectbox("Select Your Risk Profile", ("Aggressive", "Moderate"))
cash_balance = st.sidebar.number_input("Current Cash Balance", value=10000.0, step=100.0)
tax_rate = st.sidebar.slider("Estimated Capital Gains Tax Rate", 0.0, 0.4, 0.15, 0.01)

# --- Main App ---

# 1. Load Data
try:
    portfolio = create_portfolio_state('data/sample_holdings.csv', cash_balance)
except FileNotFoundError:
    st.error("Error: `data/sample_holdings.csv` not found. Please create it.")
    st.stop()


# 2. Display Current State
st.header("Current Portfolio")
holdings_df = pd.DataFrame([h.__dict__ for h in portfolio.holdings])
st.write(f"**Cash:** ${portfolio.cash:,.2f}")
st.dataframe(holdings_df)


# 3. Run Engine and Display Recommendations
st.header("💡 Recommendations")
if st.button("Generate Recommendations"):
    with st.spinner("Running Optimization Engine..."):
        recommendations = generate_recommendations(portfolio, risk_profile, tax_rate)

        if not recommendations:
            st.success("No actions are recommended at this time. Your portfolio is optimized!")
        else:
            recs_df = pd.DataFrame(recommendations)
            st.dataframe(recs_df)

            # Display Impact Analysis
            st.subheader("Impact Analysis")
            total_harvested = 0
            for rec in recommendations:
                if "Harvest" in rec['reason']:
                    # Extract loss amount from the string
                    loss_str = rec['reason'].split('$')[1].split(' ')[0]
                    total_harvested += float(loss_str)
            
            if total_harvested > 0:
                st.metric(
                    label="Total Loss Harvested",
                    value=f"${total_harvested:,.2f}",
                    help="Selling securities at a loss to offset capital gains taxes."
                )
                st.metric(
                    label="Estimated Tax Savings",
                    value=f"${total_harvested * tax_rate:,.2f}",
                    help=f"Based on your {tax_rate*100}% tax rate."
                )