import pandas as pd
from typing import Dict, List
from datetime import datetime
from .fifo_calculator import get_inr_conversion_rate

def generate_loss_harvesting_report(acq_status_df: pd.DataFrame, latest_price: float, ttbr_rates: Dict, warnings: List) -> pd.DataFrame:
    """Identifies vested shares with unrealized losses."""
    if latest_price == 0: return pd.DataFrame()
    
    harvestable = acq_status_df[acq_status_df['Remaining_Shares'] > 0].copy()
    if harvestable.empty: return pd.DataFrame()
    
    harvestable['Current_Market_Price_USD'] = latest_price
    latest_rate_key, latest_rate = get_inr_conversion_rate(datetime.now(), ttbr_rates, warnings)
    
    harvestable['Current_Market_Value_INR'] = harvestable['Current_Market_Price_USD'] * harvestable['Remaining_Shares'] * latest_rate
    
    original_cost_inr = []
    for row in harvestable.itertuples():
        acq_rate_key, acq_rate = get_inr_conversion_rate(row.Acquisition_Date, ttbr_rates, warnings)
        original_cost_inr.append(row.Acquisition_Price * row.Remaining_Shares * acq_rate)
    harvestable['Original_Cost_of_Remaining_INR'] = original_cost_inr
    
    harvestable['Unrealized_Gain_Loss_INR'] = harvestable['Current_Market_Value_INR'] - harvestable['Original_Cost_of_Remaining_INR']
    
    harvestable = harvestable[harvestable['Unrealized_Gain_Loss_INR'] < 0]
    
    return harvestable[['Acquisition_Date', 'Remaining_Shares', 'Acquisition_Price', 'Current_Market_Price_USD', 'Unrealized_Gain_Loss_INR']].sort_values(by='Unrealized_Gain_Loss_INR')