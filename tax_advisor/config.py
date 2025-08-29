# --- User Configuration ---
# Enter estimated income from other sources (e.g., salary) for accurate surcharge calculation.
INCOME_FROM_OTHER_SOURCES_INR = 11000000.00  # Example: 1.1 Cr.

# --- File Configuration ---
CAPITAL_GAINS_FILE = 'Capital Gains Report.csv'
RELEASES_FILE = 'Releases Report.csv'
QUOTE_HISTORY_FILE = 'Quote History.csv'
OUTPUT_EXCEL_FILE = 'capital_gains_summary_final.xlsx'

# --- Data Sources ---
TTBR_RATES_URL = 'https://github.com/sahilgupta/sbi-fx-ratekeeper/blob/main/csv_files/SBI_REFERENCE_RATES_USD.csv'

# --- Tax Configuration (as of FY 2024-25) ---
TAX_RATES = {
    'stcg': 0.30,
    'ltcg': 0.125,
    'cess': 0.04
}

# Surcharge slabs based on total income
SURCHARGE_SLABS = {
    5000000: 0.10,   # > 50 Lakhs to 1 Cr
    10000000: 0.15,  # > 1 Cr to 2 Cr
    20000000: 0.25,  # > 2 Cr to 5 Cr
    50000000: 0.37   # > 5 Cr
}