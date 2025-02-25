import unittest
from cryptotax_summary import calculate_crypto_summary
import pandas as pd
import os

class TestCryptoSummary(unittest.TestCase):
    def setUp(self):
        # Create a sample CSV file for testing with a header at the top
        data = {
            'Transaction Type': ['Trade', 'Sell'],
            'Transaction ID': ['1', '2'],
            'Tax lot ID': ['A', 'B'],
            'Asset name': ['BTC', 'ETH'],
            'Amount': [1.0, 0.5],
            'Date Acquired': ['2024-01-01', '2024-06-01'],
            'Cost basis (USD)': [40000, 2000],
            'Date of Disposition': ['2024-12-31', '2024-12-31'],
            'Proceeds (USD)': [50000, 2500],
            'Gains (Losses) (USD)': [10000, 500],
            'Holding period (Days)': [365, 183],
            'Data source': ['Coinbase', 'Coinbase']
        }
        df = pd.DataFrame(data)

        # Write the CSV with the header at the top (no extra lines)
        df.to_csv('test_transactions.csv', index=False)

    def test_summary_calculation(self):
        # Run the summary
        summary = calculate_crypto_summary('test_transactions.csv')
        self.assertIn('short_term_gains_losses', summary)
        self.assertIn('long_term_gains_losses', summary)
        self.assertEqual(summary['short_term_gains_losses'], 500)  # Short-term gain
        self.assertEqual(summary['long_term_gains_losses'], 10000)  # Long-term gain

    def test_missing_holding_period(self):
        # Test with a CSV missing Holding period (Days), relying on dates
        data = {
            'Transaction Type': ['Sale', 'Sale'],
            'Transaction ID': ['1', '2'],
            'Tax lot ID': ['A', 'B'],
            'Asset name': ['BTC', 'ETH'],
            'Amount': [1.0, 0.5],
            'Date Acquired': ['2024-01-01', '2024-06-01'],
            'Cost basis (USD)': [40000, 2000],
            'Date of Disposition': ['2024-12-31', '2024-12-31'],
            'Proceeds (USD)': [50000, 2500],
            'Gains (Losses) (USD)': [10000, 500],
            'Data source': ['Exchange', 'Exchange']
        }
        df = pd.DataFrame(data)

        df.to_csv('test_transactions_no_days.csv', index=False)

        summary = calculate_crypto_summary('test_transactions_no_days.csv')
        self.assertEqual(summary['short_term_gains_losses'], 500)  # Short-term gain
        self.assertEqual(summary['long_term_gains_losses'], 10000)  # Long-term gain

        if os.path.exists('test_transactions_no_days.csv'):
            os.remove('test_transactions_no_days.csv')

    def tearDown(self):
        # Clean up: remove the test CSV file after the test
        if os.path.exists('test_transactions.csv'):
            os.remove('test_transactions.csv')

if __name__ == '__main__':
    unittest.main()