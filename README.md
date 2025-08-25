# 📈 Capital Gains & Advance Tax Calculator for Indian Taxpayers

This Python script is a comprehensive tool designed for Indian taxpayers who have capital gains from selling foreign-listed employee stock units (specifically, GOOG stocks). It automates the complex process of calculating capital gains and losses using the **First-In, First-Out (FIFO)** method and estimates the corresponding **advance tax liability** as per the latest Indian tax laws.

The script takes raw CSV reports of sales and acquisitions as input and generates a clean, multi-sheet Excel report ready for analysis and verification.

***

## ✨ Key Features

* **FIFO Capital Gains Calculation:** Automatically matches sales with the earliest acquisitions to accurately calculate profit or loss for each transaction.
* **Indian Tax Law Compliant:**
    * Correctly classifies gains as **Long-Term (LTCG)** or **Short-Term (STCG)** based on the 24-month holding period for foreign stocks.
    * Applies the latest tax rates (**12.5% for LTCG**, slab rates for STCG).
    * Implements the official **tax set-off rules** where losses are correctly adjusted against gains.
* **Advance Tax Estimation:** Calculates the advance tax installments using the correct **cumulative "pay-as-you-earn" method**, showing how much is due for each quarterly deadline.
* **Comprehensive Validation:** Performs numerous sanity and integrity checks on the input data and calculation results, printing a clear validation report.
* **Detailed Excel Report:** Generates a multi-sheet `.xlsx` file that includes:
    1.  A detailed **Profit/Loss Summary**.
    2.  A transparent **Tax Calculation** sheet showing set-offs and the final liability.
    3.  An **Advance Tax Schedule**.
    4.  The final status of all **Acquisition Lots**.
    5.  Cleaned copies of your original reports.

***

## 🚀 How to Use

1.  **Prerequisites:** You need a Python environment with the `pandas` and `openpyxl` libraries installed. Google Colab is a perfect place to run this script.
    ```bash
    pip install pandas openpyxl
    ```
2.  **Input Files:** Make sure you have the following two CSV files in the same directory as the script:
    * `Capital Gains Report.csv`
    * `Releases Report.csv`
3.  **Configure Exchange Rate:** Open the script and update the `USD_TO_INR_RATE` variable at the top to the desired exchange rate for your estimation.
    ```python
    # --- 1. CONFIGURATION ---
    USD_TO_INR_RATE = 83.50 
    ```
4.  **Run the Script:** Execute the Python script from your terminal or a Colab cell.
    ```bash
    python your_script_name.py
    ```
5.  **Get Your Report:** A new Excel file named `capital_gains_summary_final.xlsx` will be created. This file contains the complete, validated analysis.

***

## 📊 Understanding the Excel Report

The generated Excel file is designed for clarity and easy verification:

* **Profit Loss Summary:** Shows a detailed breakdown of every part of each sale, matched to an acquisition lot.
* **Tax Calculation:** This is the main summary sheet. It shows:
    * The total gross gains and losses (STCG & LTCG).
    * How losses are correctly **set off** against gains.
    * The final calculation of base tax, surcharge, and cess.
    * Your **Advance Tax Schedule** with amounts and due dates.
    * A **Validation Summary** and notes on assumptions.
* **Acquisition Lot Status:** Shows every acquisition lot and how many shares (if any) are left after all sales are accounted for. This is great for verifying the FIFO logic.
* **Original Sales/Releases Report:** Cleaned-up copies of your input data for reference.

***

## ⚠️ Disclaimer

* This script is a powerful tool for **estimation and verification**, but it is **not professional tax advice**.
* The use of a **single USD/INR exchange rate is a simplification**. For official tax filing, you must use the Telegraphic Transfer Buying Rate (TTBR) for each specific transaction date as required by Indian tax law.
* The surcharge calculation assumes a total income between ₹1 crore and ₹2 crore.
* Always consult with a qualified **Chartered Accountant** or tax professional before making any financial decisions or filing your tax returns.