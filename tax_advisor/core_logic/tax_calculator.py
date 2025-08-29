import pandas as pd
from typing import Dict, Any
from datetime import datetime
import config

def calculate_tax_liability(df: pd.DataFrame, other_income: float) -> Dict[str, Any]:
    """Calculates total tax liability based on correct Indian tax set-off rules."""
    # Separate gains and losses
    stcg = df[(df['Gain_Type'] == 'STCG') & (df['Profit/Loss (INR)'] > 0)]['Profit/Loss (INR)'].sum()
    stcl = abs(df[(df['Gain_Type'] == 'STCG') & (df['Profit/Loss (INR)'] < 0)]['Profit/Loss (INR)'].sum())
    ltcg = df[(df['Gain_Type'] == 'LTCG') & (df['Profit/Loss (INR)'] > 0)]['Profit/Loss (INR)'].sum()
    ltcl = abs(df[(df['Gain_Type'] == 'LTCG') & (df['Profit/Loss (INR)'] < 0)]['Profit/Loss (INR)'].sum())

    # Apply Set-Off Rules
    ltcg_after_ltcl = max(0, ltcg - ltcl)
    stcg_after_stcl = max(0, stcg - stcl)
    stcl_remaining = max(0, stcl - stcg)
    ltcg_after_all_setoffs = max(0, ltcg_after_ltcl - stcl_remaining)
    
    net_taxable_ltcg, net_taxable_stcg = ltcg_after_all_setoffs, stcg_after_stcl
    total_capital_gains = net_taxable_ltcg + net_taxable_stcg
    total_income = other_income + total_capital_gains
    
    # Determine Surcharge Rate
    surcharge_rate = 0.0
    for limit, rate in sorted(config.SURCHARGE_SLABS.items()):
        if total_income > limit:
            surcharge_rate = rate
    
    base_tax = (net_taxable_stcg * config.TAX_RATES['stcg']) + (net_taxable_ltcg * config.TAX_RATES['ltcg'])
    surcharge = base_tax * surcharge_rate
    cess = (base_tax + surcharge) * config.TAX_RATES['cess']
    total_tax_liability = base_tax + surcharge + cess
    
    return {
        "stcg": stcg, "stcl": stcl, "ltcg": ltcg, "ltcl": ltcl,
        "net_taxable_stcg": net_taxable_stcg, "net_taxable_ltcg": net_taxable_ltcg,
        "surcharge_rate_applied": surcharge_rate, "total_base_tax": base_tax, 
        "total_surcharge": surcharge, "total_cess": cess, "total_tax_liability": total_tax_liability
    }

def calculate_advance_tax_schedule(summary_df: pd.DataFrame, other_income: float) -> pd.DataFrame:
    """Calculates advance tax installments using the cumulative method."""
    fy_start_year = pd.Timestamp.now().year if pd.Timestamp.now().month >= 4 else pd.Timestamp.now().year - 1
    q_ends = [pd.to_datetime(f'{d}-{fy_start_year if d.split("-")[1] != "03" else fy_start_year + 1}', format='%d-%m-%Y') for d in ['15-06', '15-09', '15-12', '31-03']]
    due_dates = [d.date() for d in [pd.to_datetime(f'{d}-{fy_start_year if d.split("-")[1] != "03" else fy_start_year + 1}', format='%d-%m-%Y') for d in ['15-06', '15-09', '15-12', '15-03']]]
    
    cum_tax_q1 = calculate_tax_liability(summary_df[summary_df['Sale_Date'] <= q_ends[0]], other_income)['total_tax_liability']
    cum_tax_q2 = calculate_tax_liability(summary_df[summary_df['Sale_Date'] <= q_ends[1]], other_income)['total_tax_liability']
    cum_tax_q3 = calculate_tax_liability(summary_df[summary_df['Sale_Date'] <= q_ends[2]], other_income)['total_tax_liability']
    cum_tax_q4 = calculate_tax_liability(summary_df[summary_df['Sale_Date'] <= q_ends[3]], other_income)['total_tax_liability']

    paid_so_far = 0
    payment_q1 = cum_tax_q1 * 0.15; paid_so_far += payment_q1
    payment_q2 = (cum_tax_q2 * 0.45) - paid_so_far; paid_so_far += payment_q2
    payment_q3 = (cum_tax_q3 * 0.75) - paid_so_far; paid_so_far += payment_q3
    payment_q4 = (cum_tax_q4 * 1.00) - paid_so_far

    schedule = pd.DataFrame({'Installment Due Date': due_dates,'Amount to Pay (INR)': [payment_q1, payment_q2, payment_q3, payment_q4]})
    schedule['Amount to Pay (INR)'] = schedule['Amount to Pay (INR)'].clip(lower=0)
    return schedule