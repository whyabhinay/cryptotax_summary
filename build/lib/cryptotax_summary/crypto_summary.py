# cryptotax_summary/crypto_summary.py
import pandas as pd
import os
import sys
from datetime import datetime
import argparse

def calculate_crypto_summary(csv_path):
    """
    Calculate a summary of crypto transactions for tax purposes, categorizing gains/losses
    as short-term or long-term.

    Args:
        csv_path (str): Path to the CSV file containing crypto transaction data.
                        The CSV should have a header on row 8 (Excel row 1) and include
                        columns like 'Transaction Type', 'Transaction ID', 'Tax lot ID',
                        'Asset name', 'Amount', 'Date Acquired', 'Cost basis (USD)',
                        'Date of Disposition', 'Proceeds (USD)', 'Gains (Losses) (USD)',
                        'Holding period (Days)', 'Data source'.

    Returns:
        dict: Summary with totals for short-term and long-term gains/losses, proceeds, and cost basis.

    Raises:
        FileNotFoundError: If the CSV file is not found.
        ValueError: If the CSV format is incorrect or missing required columns.
    """
    # Check if the file exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at: {csv_path}")

    try:
        # Read the CSV, skipping rows 1-7 (Excel rows 1-7) and using row 8 as header
        df = pd.read_csv(csv_path, skiprows=7, header=0)

        # Verify required columns exist
        required_columns = ['Transaction Type', 'Transaction ID', 'Tax lot ID', 'Asset name',
                           'Amount', 'Date Acquired', 'Cost basis (USD)', 'Date of Disposition',
                           'Proceeds (USD)', 'Gains (Losses) (USD)', 'Holding period (Days)',
                           'Data source']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

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

    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty or contains no data after the header.")
    except pd.errors.ParserError:
        raise ValueError("Invalid CSV format. Ensure the file has a header on row 8 and correct data.")

def main():
    """Command-line interface for cryptotax_summary."""
    parser = argparse.ArgumentParser(description='Summarize crypto transactions from a CSV file for tax reporting.')
    parser.add_argument('csv_path', help='Path to the CSV file containing crypto transaction data.')
    args = parser.parse_args()

    try:
        summary = calculate_crypto_summary(args.csv_path)
        print("Crypto Transaction Summary:")
        print(f"Short-term Gains/Losses: ${summary['short_term_gains_losses']:,.2f}")
        print(f"Long-term Gains/Losses: ${summary['long_term_gains_losses']:,.2f}")
        print(f"Total Proceeds: ${summary['total_proceeds']:,.2f}")
        print(f"Total Cost Basis: ${summary['total_cost_basis']:,.2f}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()