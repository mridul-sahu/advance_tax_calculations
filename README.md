# 📈 Automated Capital Gains & Advance Tax Calculator

This Python-based application provides a comprehensive solution for Indian taxpayers to calculate capital gains from foreign-listed employee stock units and to estimate the corresponding advance tax liability. The software automates the entire workflow, from fetching official exchange rates to generating a fully validated, multi-sheet tax report ready for auditing and ITR filing.

The architecture is designed to be scalable and maintainable, making it an ideal foundation for a full-fledged tax advisory software.

***

## ✨ Key Features

* **Automated Exchange Rate Fetching:** Downloads the latest **SBI Telegraphic Transfer Buying Rate (TTBR)** data directly from its source. No manual rate management is needed.
* **Compliant Currency Conversion:** Implements the official tax rule by using the TTBR from the **last day of the month preceding each transaction** for ultimate accuracy.
* **Intelligent Rate Handling:** Automatically uses the most recent available rate if the exact month-end date is a holiday and logs these instances in a dedicated report sheet for full transparency.
* **Accurate Indian Tax Logic:**
    * Correctly classifies gains as **Long-Term (LTCG)** or **Short-Term (STCG)** based on the 24-month holding period.
    * Implements the official **tax set-off rules**, correctly adjusting losses against gains.
    * Calculates the final liability including surcharge (based on total income) and cess.
* **Precise Advance Tax Schedule:** Uses the correct **cumulative method** to estimate your advance tax liability for each installment deadline.
* **Financial Intelligence:** Includes a **Tax-Loss Harvesting** report to identify potential opportunities to offset gains by selling assets at an unrealized loss.
* **Comprehensive Validation:** Runs a full suite of sanity and integrity checks on all input data and calculation results, printing a clear validation report.
* **Actionable Excel Report:** Generates a detailed, multi-sheet `.xlsx` file designed for easy auditing and direct use for ITR filing.

***

## 🚀 Getting Started

### Prerequisites

You need Python 3.8+ and the required packages.

### Installation

1.  Clone the repository:
    ```bash
    git clone <your-repository-url>
    cd <your-repository-folder>
    ```

2.  Install the dependencies using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

### Execution

1.  **Place Input Files:** Ensure your `Capital Gains Report.csv`, `Releases Report.csv`, and `Quote History.csv` files are in the root directory of the project.

2.  **Configure Your Income:** Open the `config.py` file and set the `INCOME_FROM_OTHER_SOURCES_INR` variable to your estimated annual income from other sources (like salary) for an accurate surcharge calculation.

3.  **Run the Application:** Execute the `main.py` script from your terminal.
    ```bash
    python main.py
    ```
4.  **Get Your Report:** A new Excel file named `capital_gains_summary_final.xlsx` will be created in the root directory. This file contains the complete, validated analysis.

***

## 📊 Understanding the Excel Report

The generated Excel file is designed to be a complete, self-explanatory audit trail:

* **Profit Loss Summary:** The most detailed sheet. For every transaction slice, it shows the USD prices, the **exact TTBRs used** for sale and acquisition, the resulting **INR proceeds and costs**, and the final profit/loss.
* **Tax Calculation Explained:** A dedicated sheet with a step-by-step guide in plain English explaining how the currency conversion and tax liability are calculated according to Indian tax law, with direct references to ITR-2 form schedules.
* **Tax Calculation:** The main summary sheet showing the set-off of gains/losses, the final tax liability, the advance tax schedule, and a summary of all validation checks.
* **Tax Loss Harvesting:** An actionable report showing vested shares currently at a loss, which could potentially be sold to offset gains.
* **TTBR Rates Used & Warnings:** Audit trail sheets listing every unique TTBR that was used and any fallbacks that were necessary due to holidays.
* **Acquisition Lot Status:** Shows every acquisition lot, the **total shares sold** from it, and the **total shares remaining**, providing a clear view of the FIFO process.

***

## ⚠️ Disclaimer

* This software is a powerful tool for **estimation and verification**, but it is **not professional tax advice**.
* The accuracy of the calculation is dependent on the correctness of your input reports and the data in the TTBR source repository.
* Always consult with a qualified **Chartered Accountant** or tax professional before making any financial decisions or filing your tax returns.