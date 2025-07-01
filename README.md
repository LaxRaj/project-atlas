# Project Atlas 🚀

A portfolio optimization engine to maximize after-tax returns through tax-loss harvesting and goal-based asset allocation. This project was built as a demonstration of financial engineering and software development skills.

## ✨ Features

* **Tax-Loss Harvesting (TLH):** Identifies and recommends trades to harvest capital losses, reducing tax liability.
* **Goal-Based Rebalancing:** Keeps the portfolio aligned with a target asset allocation based on the user's risk profile.
* **Wash Sale Rule Compliance:** Ensures all recommended sales will not violate the 61-day wash sale rule.
* **Simple UI:** A Streamlit-based interface to display portfolio state and actionable recommendations.

## 🛠️ Tech Stack

* **Backend:** Python
* **Data Analysis:** Pandas, NumPy
* **Frontend/UI:** Streamlit
* **API Simulation:** Data loaded from local CSV files, simulating a Plaid API connection.

## ⚙️ Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/project-atlas.git](https://github.com/your-username/project-atlas.git)
    cd project-atlas
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install -e .
    ```

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```