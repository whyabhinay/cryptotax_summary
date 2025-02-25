# CryptoTax Summary Library

A Python library that summarizes **Coinbase** crypto transaction data for IRS tax reporting. It categorizes gains and losses as short-term or long-term and is tailored for **U.S. tax filers with more than 4,000 transactions—exceeding TurboTax’s upload limits.** This tool simplifies the calculation of **short-term gains, long-term gains, total proceeds, and total cost basis.**

## Important Note

Ensure that you use the Gain/Loss Statement as the input file for accurate processing.

## Disclaimer

Please note that you may still be required to mail your Gain/Loss statement to the IRS. I am not a tax professional; therefore, please consult a qualified tax expert for guidance on your tax filing and any additional questions.

## Installation

```bash
pip install cryptotax_summary
```

## Usage

Command-Line Interface
Run the library directly from the command line with your CSV file:

```bash
cryptotax_summary CB-GAINLOSSCSV.csv
```

## Example
