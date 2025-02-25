import pandas as pd
import os
import sys
from datetime import datetime
import argparse

def classify_holding_period(date_acquired_str, date_disposed_str):
    """
    Determine if a holding period is short-term or long-term based on acquisition and disposition dates.

    Args:
        date_acquired_str (str): Date the asset was acquired (e.g., '2024-01-01').
        date_disposed_str (str): Date the asset was disposed of (e.g., '2024-12-31').

    Returns:
        str: 'Short-term' if held < 365 days, 'Long-term' otherwise.
    """
    try:
        # Explicitly specify the date format to avoid ambiguity
        date_acquired = pd.to_datetime(date_acquired_str, format='%Y-%m-%d', utc=True)
        date_disposed = pd.to_datetime(date_disposed_str, format='%Y-%m-%d', utc=True)
        # Calculate the holding period in days, ensuring whole days
        holding_days = (date_disposed.date() - date_acquired.date()).days
        print(f"Debug: Holding days for {date_acquired.date()} to {date_disposed.date()}: {holding_days}")
        return 'Short-term' if holding_days < 365 else 'Long-term'
    except Exception as e:
        print(f"Error processing dates: {e}")
        return None

def calculate_crypto_summary(csv_path):
    """
    Calculate a summary of crypto transactions for tax purposes, categorizing gains/losses
    as short-term or long-term.

    Args:
        csv_path (str): Path to the CSV file containing crypto transaction data.
                        The CSV should include columns like 'Transaction Type', 'Transaction ID',
                        'Tax lot ID', 'Asset name', 'Amount', 'Date Acquired', 'Cost basis (USD)',
                        'Date of Disposition', 'Proceeds (USD)', 'Gains (Losses) (USD)',
                        'Holding period (Days)' (optional), 'Data source'. The header can be anywhere in the file.

    Returns:
        dict: Summary with totals for short-term and long-term gains/losses, proceeds, and cost basis.

    Raises:
        FileNotFoundError: If the CSV file is not found.
        ValueError: If required columns are missing or the CSV format is invalid.
    """
    # Check if the file exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at: {csv_path}")

    try:
        # Read the CSV without assuming the header position, letting pandas infer it
        df = pd.read_csv(csv_path)

        # Define strictly required columns (excluding 'Holding period (Days)')
        required_columns = ['Transaction Type', 'Transaction ID', 'Tax lot ID', 'Asset name',
                           'Amount', 'Date Acquired', 'Cost basis (USD)', 'Date of Disposition',
                           'Proceeds (USD)', 'Gains (Losses) (USD)', 'Data source']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Debug: Print the DataFrame to check data
        print("DataFrame after reading CSV:")
        print(df)

        # Ensure 'Holding period (Days)' is numeric if it exists
        if 'Holding period (Days)' in df.columns:
            df['Holding period (Days)'] = pd.to_numeric(df['Holding period (Days)'], errors='coerce')

        # Use 'Holding period (Days)' if present and not all NaN, otherwise fall back to date-based classification
        if 'Holding period (Days)' in df.columns and not df['Holding period (Days)'].isna().all():
            df['Holding period'] = df['Holding period (Days)'].apply(
                lambda days: 'Short-term' if pd.notna(days) and days < 365 else 'Long-term'
            )
        else:
            if 'Date Acquired' not in df.columns or 'Date of Disposition' not in df.columns:
                raise ValueError("Missing 'Date Acquired' or 'Date of Disposition' for date-based holding period calculation.")
            df['Holding period'] = df.apply(
                lambda row: classify_holding_period(row['Date Acquired'], row['Date of Disposition']),
                axis=1
            )

        # Debug: Print the DataFrame with the new 'Holding period' column
        print("DataFrame after adding Holding period:")
        print(df)

        # Calculate totals for gains/losses by holding period
        summary = df.groupby('Holding period')['Gains (Losses) (USD)'].sum().to_dict()
        print("Summary before finalizing:")
        print(summary)

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
        print("Final Summary:")
        print(result)
        return result

    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty or contains no data after the header.")
    except pd.errors.ParserError:
        raise ValueError("Invalid CSV format. Please ensure the file is a valid CSV with a header row.")

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