import pandas as pd

def generate_excel_report(output_file, **kwargs):
    """Writes all the calculated dataframes to a formatted, multi-sheet Excel file."""
    tax_explanation = [
        ("How Your Tax Is Calculated: A Step-by-Step Guide", ""),
        ("Step 1: Convert all USD Transactions to INR", "This is the most critical step. All USD amounts are converted to INR using the official method prescribed by Indian Tax Law."),
        ("   - The Rule (Rule 115):", "The USD amount is converted using the Telegraphic Transfer Buying Rate (TTBR) from the State Bank of India (SBI)."),
        ("   - The Date:", "The specific rate used is from the *last day of the month immediately preceding the month* of the transaction."),
        ("   - In this report:", "The 'Profit Loss Summary' and 'TTBR Rates Used' sheets provide a full, transparent audit trail of this process."),
        ("", ""),
        ("Step 2: Apply Tax Set-Off Rules", "Losses are used to offset gains in a specific order to determine the final taxable income."),
        ("   - Long-Term Capital Loss (LTCL):", "Can ONLY be set off against Long-Term Capital Gains (LTCG)."),
        ("   - Short-Term Capital Loss (STCL):", "Is first set off against Short-Term Capital Gains (STCG). Any remaining STCL can then offset LTCG."),
        ("Step 3: Calculate Total Tax Liability", "The final tax is calculated on the 'Net Taxable Gains' after set-off, including Surcharge and Cess."),
        ("", ""),
        ("How this report helps with ITR Filing (Form ITR-2):", ""),
        ("   - Schedule CG:", "The 'Net Taxable STCG' and 'Net Taxable LTCG' from the 'Tax Calculation' sheet are the primary figures for this schedule."),
        ("   - Schedule BFLA (Brought Forward Losses Adjustment):", "If you have losses from previous years, they would be adjusted here. This script calculates the current year's position."),
    ]
    
    notes_list = [
        ("NOTES:", ""),
        ("1. Exchange Rate:", "Date-specific TTBRs downloaded and used as per Indian Tax Law."),
        ("2. Surcharge:", f"A rate of {kwargs['tax_data']['surcharge_rate_applied']*100:.0f}% was applied based on your total estimated income."),
        ("3. Tax Loss Harvesting:", "This sheet identifies potential losses you could realize to offset gains. It is a suggestion, not financial advice."),
        ("", ""),
        ("VALIDATION SUMMARY:", ""),
        ("Share Count Match:", f"{kwargs['validation_results']['Share Match']}"),
        ("Overselling Check:", f"{kwargs['validation_results']['Overselling']}"),
        ("Tax Integrity Check:", f"{kwargs['validation_results']['Tax Integrity']}"),
    ]

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        kwargs['summary_df'].to_excel(writer, sheet_name='Profit Loss Summary', index=False)
        pd.DataFrame(tax_explanation).to_excel(writer, sheet_name='Tax Calculation Explained', index=False, header=False)
        if not kwargs['warnings_df'].empty:
            kwargs['warnings_df'].to_excel(writer, sheet_name='TTBR Warnings', index=False)
        if not kwargs['loss_harvesting_df'].empty:
            kwargs['loss_harvesting_df'].to_excel(writer, sheet_name='Tax Loss Harvesting', index=False)
        
        # Build Main Tax Sheet
        current_row = 0
        set_off_summary = pd.DataFrame({'Category': ['Short-Term', 'Long-Term'],'Gross Gains (INR)': [kwargs['tax_data']['stcg'], kwargs['tax_data']['ltcg']],'Gross Losses (INR)': [kwargs['tax_data']['stcl'], kwargs['tax_data']['ltcl']],'Net Taxable Gains (INR)': [kwargs['tax_data']['net_taxable_stcg'], kwargs['tax_data']['net_taxable_ltcg']]})
        tax_summary = pd.DataFrame({'Description': ['Total Base Tax', 'Total Surcharge', 'Total Health & Education Cess', 'TOTAL TAX LIABILITY'],'Amount (INR)': [kwargs['tax_data']['total_base_tax'], kwargs['tax_data']['total_surcharge'], kwargs['tax_data']['total_cess'], kwargs['tax_data']['total_tax_liability']]})
        pd.DataFrame([['TAX SET-OFF CALCULATION']]).to_excel(writer, sheet_name='Tax Calculation', index=False, header=False, startrow=current_row); current_row += 1
        set_off_summary.to_excel(writer, sheet_name='Tax Calculation', index=False, startrow=current_row); current_row += len(set_off_summary) + 2
        pd.DataFrame([['FINAL TAX LIABILITY']]).to_excel(writer, sheet_name='Tax Calculation', index=False, header=False, startrow=current_row); current_row += 1
        tax_summary.to_excel(writer, sheet_name='Tax Calculation', index=False, startrow=current_row); current_row += len(tax_summary) + 2
        pd.DataFrame([['ADVANCE TAX PAYMENT SCHEDULE']]).to_excel(writer, sheet_name='Tax Calculation', index=False, header=False, startrow=current_row); current_row += 1
        kwargs['schedule_df'].to_excel(writer, sheet_name='Tax Calculation', index=False, startrow=current_row); current_row += len(kwargs['schedule_df']) + 2
        pd.DataFrame(notes_list).to_excel(writer, sheet_name='Tax Calculation', index=False, header=False, startrow=current_row)

        kwargs['used_rates_df'].to_excel(writer, sheet_name='TTBR Rates Used', index=False)
        kwargs['sales_df'].to_excel(writer, sheet_name='Original Sales Report', index=False)
        kwargs['acq_df'].to_excel(writer, sheet_name='Original Releases Report', index=False)
        
        acq_status_df = kwargs['acq_status_df'][['Acquisition_Date', 'Shares_Acquired', 'Shares_Sold_from_Lot', 'Remaining_Shares']]
        acq_status_df.to_excel(writer, sheet_name='Acquisition Lot Status', index=False)

    print(f"\n✅ Success! The '{output_file}' has been created with all validations and supercharged features.")