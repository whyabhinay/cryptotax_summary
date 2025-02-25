import unittest
from cryptotax_summary import calculate_crypto_summary

class TestCryptoSummary(unittest.TestCase):
    def test_summary_calculation(self):
        # Create a sample CSV file for testing
        import pandas as pd
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
            'Holding period (Days)': [365, 183],
            'Data source': ['Exchange', 'Exchange']
        }
        df = pd.DataFrame(data)
        df.to_csv('test_transactions.csv', index=False)

        # Run the summary
        summary = calculate_crypto_summary('test_transactions.csv')
        self.assertIn('short_term_gains_losses', summary)
        self.assertIn('long_term_gains_losses', summary)
        self.assertEqual(summary['short_term_gains_losses'], 500)  # Short-term gain
        self.assertEqual(summary['long_term_gains_losses'], 10000)  # Long-term gain

if __name__ == '__main__':
    unittest.main()