import pandas as pd
import numpy as np
from typing import Any, Dict

def clean_currency(value: Any) -> float:
    """Removes currency symbols and commas, then converts to float."""
    if isinstance(value, str):
        return float(value.replace('$', '').replace(',', ''))
    return float(value)

def perform_validations(sales_df: pd.DataFrame, acq_df: pd.DataFrame, summary_df: pd.DataFrame, acq_status_df: pd.DataFrame, tax_data: Dict) -> Dict:
    """Runs a comprehensive set of checks and returns the results."""
    print("\n--- Running Final Calculation Validations ---")
    
    # Input Data Sanity Checks
    sanity_errors = False
    if sales_df.empty:
        print("🟡 Sanity Check: Capital Gains Report is empty."); sanity_errors = True
    if acq_df.empty:
        print("❌ Sanity Check Fail: Releases Report is empty."); sanity_errors = True
    
    # Post-Calculation Checks
    total_shares_sold_original = sales_df['Shares_Sold'].sum()
    total_shares_sold_summary = summary_df['Shares_Sold'].sum()
    share_match = np.isclose(total_shares_sold_original, total_shares_sold_summary)
    print(f"Share Count Match (Original vs Summary): {'✅ Pass' if share_match else '❌ Fail'}")

    oversold = (acq_status_df['Remaining_Shares'] < -1e-4).any()
    print(f"Overselling Check (No negative shares): {'✅ Pass' if not oversold else '❌ Fail'}")

    tax_check = np.isclose(
        tax_data['total_base_tax'] + tax_data['total_surcharge'] + tax_data['total_cess'],
        tax_data['total_tax_liability']
    )
    print(f"Tax Calculation Integrity (Components Sum to Total): {'✅ Pass' if tax_check else '❌ Fail'}")
    print("-----------------------------------------")
    
    return {
        "Sanity Checks": 'Pass' if not sanity_errors else 'Fail',
        "Share Match": 'Pass' if share_match else 'Fail',
        "Overselling": 'Pass' if not oversold else 'Fail',
        "Tax Integrity": 'Pass' if tax_check else 'Fail',
    }