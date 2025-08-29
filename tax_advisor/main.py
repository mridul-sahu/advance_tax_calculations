# tax_advisor/main.py

import pandas as pd
import config
from data_loader.loader import download_and_load_ttbr_rates, load_and_clean_data
from core_logic.fifo_calculator import perform_fifo_matching
from core_logic.tax_calculator import calculate_tax_liability, calculate_advance_tax_schedule
from core_logic.financial_strategy import generate_loss_harvesting_report
from reporting.excel_report import generate_excel_report
from utils.helpers import perform_validations

def main():
    """Main function to run the entire capital gains and tax calculation process."""
    try:
        # Step 1: Load all data
        ttbr_rates = download_and_load_ttbr_rates(config.TTBR_RATES_URL)
        sales_df, acq_df, latest_price = load_and_clean_data(
            config.CAPITAL_GAINS_FILE, config.RELEASES_FILE, config.QUOTE_HISTORY_FILE
        )
        
        # Step 2: Perform calculations
        summary_df, acq_status_df, used_rates, warnings = perform_fifo_matching(sales_df, acq_df, ttbr_rates)
        used_rates_df = pd.DataFrame(list(used_rates.items()), columns=['Date', 'TTBR']).sort_values('Date')
        warnings_df = pd.DataFrame(warnings).drop_duplicates().reset_index(drop=True)
        tax_data = calculate_tax_liability(summary_df, config.INCOME_FROM_OTHER_SOURCES_INR)
        advance_tax_schedule = calculate_advance_tax_schedule(summary_df, config.INCOME_FROM_OTHER_SOURCES_INR)
        loss_harvesting_df = generate_loss_harvesting_report(acq_status_df, latest_price, ttbr_rates, warnings)

        # Step 3: Run all validations
        validation_results = perform_validations(sales_df, acq_df, summary_df, acq_status_df, tax_data)
        
        # Step 4: Generate the final Excel report
        generate_excel_report(
            output_file=config.OUTPUT_EXCEL_FILE,
            summary_df=summary_df,
            acq_status_df=acq_status_df,
            tax_data=tax_data,
            schedule_df=advance_tax_schedule,
            used_rates_df=used_rates_df,
            warnings_df=warnings_df,
            loss_harvesting_df=loss_harvesting_df,
            sales_df=sales_df,
            acq_df=acq_df,
            validation_results=validation_results
        )
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please check your input files and the script configuration.")

if __name__ == '__main__':
    main()