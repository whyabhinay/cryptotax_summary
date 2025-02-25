import pandas as pd
from datetime import datetime

def calculate_crypto_summary(csv_path):
    """
    Calculate a summary of crypto transactions for tax purposes, categorizing gains/losses
    as short-term or long-term.

    Args:
        csv_path (str): Path to the CSV file containing crypto transaction data.

    Returns:
        dict: Summary with totals for short-term and long-term gains/losses, proceeds, and cost basis.
    """
    # Read the CSV file
    df = pd.read_csv(csv_path, skiprows=7, header=0)

    # Function to determine if a holding period is short-term or long-term
    def classify_holding_period(date_acquired_str, date_disposed_str):
        try:
            date_acquired = pd.to_datetime(date_acquired_str)
            date_disposed = pd.to_datetime(date_disposed_str)
            holding_days = (date_disposed - date_acquired).days
            return 'Short-term' if holding_days <= 365 else 'Long-term'
        except Exception as e:
            print(f"Error processing dates: {e}")
            return None

    # Verify or use existing 'Holding period (Days)' column
    if 'Holding period' not in df.columns:
        df['Holding period'] = df.apply(
            lambda row: classify_holding_period(row['Date Acquired'], row['Date of Disposition']),
            axis=1
        )
    else:
        df['Holding period'] = df['Holding period (Days)'].apply(
            lambda days: 'Short-term' if days <= 365 else 'Long-term'
        )

    # Calculate totals for gains/losses by holding period
    summary = df.groupby('Holding period')['Gains (Losses) (USD)'].sum().to_dict()

    # Additional totals for TurboTax
    total_proceeds = df['Proceeds (USD)'].sum()
    total_cost_basis = df['Cost basis (USD)'].sum()

    # Combine results into a dictionary
    result = {
        'short_term_gains_losses': summary.get('Short-term', 0),
        'long_term_gains_losses': summary.get('Long-term', 0),
        'total_proceeds': total_proceeds,
        'total_cost_basis': total_cost_basis
    }
    return result