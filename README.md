# 📈 Automated Capital Gains & Advance Tax Calculator for Indian Taxpayers

This Python script is a definitive, end-to-end tool for Indian taxpayers with capital gains from selling foreign-listed employee stock units. It automates the entire process, from fetching official exchange rates to generating a fully validated, multi-sheet tax report.

The script is designed for maximum accuracy and transparency, implementing the **First-In, First-Out (FIFO)** method for capital gains and adhering to the latest **Indian tax laws** for calculation and reporting.

***

## ✨ Key Features

* **Automated Exchange Rate Fetching:** Downloads the latest **SBI Telegraphic Transfer Buying Rate (TTBR)** data directly from its source on GitHub. No manual rate management is needed.
* **Compliant Currency Conversion:** Implements the official tax rule by using the TTBR from the **last day of the month preceding each transaction** for ultimate accuracy.
* **Intelligent Rate Handling:** Automatically uses the most recent available rate if the exact month-end date is a holiday, and logs these instances for full transparency.
* **Accurate Indian Tax Logic:**
    * Correctly classifies gains as **Long-Term (LTCG)** or **Short-Term (STCG)** based on the 24-month holding period.
    * Applies the official **tax set-off rules**, correctly adjusting losses against gains.
    * Calculates the final liability including surcharge and cess.
* **Precise Advance Tax Schedule:** Uses the correct **cumulative method** to estimate your advance tax liability for each installment deadline.
* **Comprehensive Validation:** Runs a full suite of sanity and integrity checks on your input data and all calculation results, printing a clear validation report.
* **Ultra-Transparent Excel Report:** Generates a detailed, multi-sheet `.xlsx` file designed for easy auditing and verification.

***

## 🚀 How to Use

1.  **Prerequisites:** You need a Python environment with the `pandas` and `requests` libraries installed. Google Colab is a perfect place to run this script.
    ```bash
    pip install pandas requests
    ```
2.  **Input Files:** Place the following two CSV files in the same directory as the script:
    * `Capital Gains Report.csv`
    * `Releases Report.csv`
3.  **Run the Script:** Execute the Python script from your terminal or a Colab cell. It will handle downloading the exchange rates automatically.
    ```bash
    python your_script_name.py
    ```
4.  **Get Your Report:** A new Excel file named `capital_gains_summary_final.xlsx` will be created. This file contains the complete, validated analysis.

***

## 📊 Understanding the Excel Report

The generated Excel file is designed to be a complete, self-explanatory audit trail:

* **Profit Loss Summary:** The most detailed sheet. For every transaction slice, it shows the USD prices, the **exact TTBRs used** for sale and acquisition, the resulting **INR proceeds and costs**, and the final profit/loss.
* **Tax Calculation Explained:** A dedicated sheet with a step-by-step guide in plain English explaining how the currency conversion and tax liability are calculated according to Indian tax law.
* **Tax Calculation:** The main summary sheet showing the set-off of gains/losses, the final tax liability, the advance tax schedule, and a summary of all validation checks.
* **TTBR Rates Used:** A reference sheet listing every unique TTBR that was looked up and used in your calculations.
* **TTBR Warnings:** An important audit log that shows if and when the script had to use a fallback date for an exchange rate (e.g., due to a weekend or holiday).
* **Acquisition Lot Status:** Shows every acquisition lot, the **total shares sold** from it, and the **total shares remaining**, providing a clear view of the FIFO process.
* **Original Reports:** Cleaned-up copies of your input data for reference.

***

## ⚠️ Disclaimer

* This script is a powerful tool for **estimation and verification**, but it is **not professional tax advice**.
* The accuracy of the calculation is dependent on the completeness and correctness of your input reports and the availability of historical rates in the source GitHub repository.
* The surcharge calculation assumes a total income between ₹1 crore and ₹2 crore.
* Always consult with a qualified **Chartered Accountant** or tax professional before making any financial decisions or filing your tax returns.
