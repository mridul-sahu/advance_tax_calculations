import pandas as pd
from typing import Tuple, Dict, List
from datetime import datetime, timedelta

def get_inr_conversion_rate(transaction_date: datetime, rates: Dict[str, float], warnings: List) -> Tuple[str, float]:
    """Finds the TTBR for a transaction, with fallback for weekends/holidays."""
    rate_date = transaction_date - pd.DateOffset(months=1)
    rate_date_eomonth = rate_date + pd.offsets.MonthEnd(0)
    
    current_date = rate_date_eomonth
    for _ in range(7):
        rate_key = current_date.strftime('%Y-%m-%d')
        if rate_key in rates:
            if current_date != rate_date_eomonth:
                warnings.append({
                    'Required Date': rate_date_eomonth.strftime('%Y-%m-%d'),
                    'Fallback Date Used': rate_key,
                    'Rate': rates[rate_key],
                    'Reason': 'Exact month-end rate not available (likely holiday/weekend).'
                })
            return rate_key, rates[rate_key]
        current_date -= timedelta(days=1)
        
    raise ValueError(f"CRITICAL: Missing TTBR rate for required date: '{rate_date_eomonth.strftime('%Y-%m-%d')}'")

def perform_fifo_matching(sales_df: pd.DataFrame, acq_df: pd.DataFrame, ttbr_rates: Dict) -> Tuple[pd.DataFrame, pd.DataFrame, Dict, List]:
    """Matches sales to acquisitions using FIFO and calculates profit/loss."""
    acquisitions_info = acq_df[['Vest_Date', 'Acquisition_Price', 'Shares_Acquired']].copy()
    acquisitions_info.rename(columns={'Vest_Date': 'Acquisition_Date'}, inplace=True)
    acquisitions_info['Remaining_Shares'] = acquisitions_info['Shares_Acquired']

    results_list, used_rates, warnings = [], {}, []
    current_acq_index = 0

    for sale in sales_df.itertuples():
        shares_to_match = sale.Shares_Sold
        for acq_index in range(current_acq_index, len(acquisitions_info)):
            if shares_to_match <= 1e-4: break
            if acquisitions_info.loc[acq_index, 'Acquisition_Date'] > sale.Sale_Date: continue

            shares_from_lot = min(shares_to_match, acquisitions_info.loc[acq_index, 'Remaining_Shares'])
            if shares_from_lot > 0:
                acq = acquisitions_info.loc[acq_index]
                
                sale_rate_key, sale_rate = get_inr_conversion_rate(sale.Sale_Date, ttbr_rates, warnings)
                acq_rate_key, acq_rate = get_inr_conversion_rate(acq.Acquisition_Date, ttbr_rates, warnings)
                used_rates.update({acq_rate_key: acq_rate, sale_rate_key: sale_rate})

                cost_inr = (acq.Acquisition_Price * shares_from_lot) * acq_rate
                proceeds_inr = (sale.Sale_Price * shares_from_lot) * sale_rate
                
                results_list.append({
                    'Sale_Date': sale.Sale_Date, 'Shares_Sold': shares_from_lot,
                    'Sale_Price_USD': sale.Sale_Price, 'Acquisition_Price_USD': acq.Acquisition_Price,
                    'Sale_TTBR': sale_rate, 'Acquisition_TTBR': acq_rate,
                    'Sale_Proceeds_INR': proceeds_inr, 'Cost_of_Acquisition_INR': cost_inr,
                    'Profit/Loss (INR)': proceeds_inr - cost_inr,
                    'Holding Duration (Days)': (sale.Sale_Date - acq.Acquisition_Date).days,
                    'Gain_Type': 'LTCG' if (sale.Sale_Date - acq.Acquisition_Date).days > 730 else 'STCG'
                })
                
                acquisitions_info.loc[acq_index, 'Remaining_Shares'] -= shares_from_lot
                shares_to_match -= shares_from_lot

            if acquisitions_info.loc[acq_index, 'Remaining_Shares'] <= 1e-4:
                current_acq_index += 1

    summary_df = pd.DataFrame(results_list)
    acquisitions_info['Shares_Sold_from_Lot'] = acquisitions_info['Shares_Acquired'] - acquisitions_info['Remaining_Shares']
    return summary_df, acquisitions_info, used_rates, warnings