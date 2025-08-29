import pandas as pd
import requests
import io
from typing import Tuple, Dict
from datetime import datetime, timedelta
from utils.helpers import clean_currency

def download_and_load_ttbr_rates(url: str) -> Dict[str, float]:
    """Downloads the TTBR rates CSV and loads it into a dictionary."""
    print(f"Downloading TTBR rates from source...")
    try:
        raw_url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        response = requests.get(raw_url)
        response.raise_for_status()
        
        rates_df = pd.read_csv(io.StringIO(response.text))
        rates_df['DATE'] = pd.to_datetime(rates_df['DATE'])
        
        print("✅ TTBR rates downloaded successfully.")
        return pd.Series(rates_df['TT BUY'].values, index=rates_df['DATE'].dt.strftime('%Y-%m-%d')).to_dict()
    except Exception as e:
        raise ConnectionError(f"Failed to download or parse the exchange rate file. Error: {e}")

def load_and_clean_data(sales_file: str, acq_file: str, quote_file: str) -> Tuple[pd.DataFrame, pd.DataFrame, float]:
    """Loads and cleans all necessary local input files."""
    try:
        sales_df = pd.read_csv(sales_file, skiprows=2, skipfooter=1, engine='python')
        acq_df = pd.read_csv(acq_file, skiprows=1, skipfooter=1, engine='python')
        quote_df = pd.read_csv(quote_file, skiprows=1).dropna(how='all')
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e}. Ensure all CSVs are in the correct path.") from e

    # Clean data
    sales_df.dropna(how='all', inplace=True)
    acq_df.dropna(how='all', inplace=True)
    sales_df.columns = ['Sale_Date', 'Sale_Price', 'Shares_Sold', 'Symbol', 'Gross_Proceeds', 'Acquisition_Date_in_Report']
    acq_df.columns = ['Vest_Date', 'Order_Number', 'Plan', 'Type', 'Status', 'Acquisition_Price', 'Quantity', 'Net_Cash_Proceeds', 'Shares_Acquired', 'Tax_Payment_Method']
    
    for col in ['Sale_Price', 'Gross_Proceeds', 'Acquisition_Price', 'Net_Cash_Proceeds']:
        df = sales_df if col in sales_df.columns else acq_df
        df[col] = df[col].apply(clean_currency)
    
    sales_df['Shares_Sold'] = pd.to_numeric(sales_df['Shares_Sold'])
    acq_df['Shares_Acquired'] = pd.to_numeric(acq_df['Shares_Acquired'])
    sales_df['Sale_Date'] = pd.to_datetime(sales_df['Sale_Date'])
    acq_df['Vest_Date'] = pd.to_datetime(acq_df['Vest_Date'])

    quote_df.columns = ['Fund', 'Quote_Date', 'Price']
    quote_df = quote_df[quote_df['Fund'].str.contains("GOOG", na=False)]
    quote_df['Price'] = quote_df['Price'].apply(clean_currency)
    latest_price = quote_df['Price'].iloc[-1] if not quote_df.empty else 0

    return sales_df.sort_values(by='Sale_Date').reset_index(drop=True), acq_df.sort_values(by='Vest_Date').reset_index(drop=True), latest_price