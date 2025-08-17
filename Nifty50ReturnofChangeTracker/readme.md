---

## 📄 README.md

````markdown
# 📊 NIFTY50 30-Day ROC Analysis & Report Generator

This project analyzes the **NIFTY50 stocks** using **Rate of Change (ROC)** over the last 30 days, identifies the **top gainers** and **top losers**, and generates a professional **multi-page PDF report**, along with **CSV** and **Excel** summaries.

---

## 🚀 Features
- Fetches **1 year of historical stock data** for all NIFTY50 tickers from [Yahoo Finance](https://finance.yahoo.com/).
- Calculates **30-day ROC (%)** for each stock.
- Identifies **Top N Gainers** and **Top N Losers** (default: 10).
- Generates:
  - **CSV Summary** (`nifty_roc_summary.csv`)
  - **Excel Summary** (`nifty_roc_summary.xlsx`)
  - **PDF Report** (`nifty_roc_report_YYYY-MM-DD.pdf`)
    - Individual ROC charts for each stock
    - Bar chart of **Top Gainers vs Losers**
    - Summary table (color-coded: green = gainers, red = losers)
- Saves a **sample chart image** (`example_chart.png`) for README usage.

---

## 📦 Requirements
- Python 3.8+
- Libraries:
  ```bash
  pip install yfinance pandas matplotlib openpyxl
````

---

## 🛠️ How to Run

1. Clone this repo or copy the script.
2. Run the script:

   ```bash
   python nifty50_roc_report.py
   ```
3. Outputs will be saved in the `./output` folder:

   * `nifty_roc_summary.csv`
   * `nifty_roc_summary.xlsx`
   * `nifty_roc_report_YYYY-MM-DD.pdf`
   * `example_chart.png`

---

## 📑 Example Report Pages

1. **Individual ROC Chart**

   * Shows how each stock’s 30-day ROC has moved over time.
2. **Top 10 Gainers vs Top 10 Losers**

   * Green bars = Gainers
   * Red bars = Losers
   * Annotated with ROC values
3. **Summary Table**

   * Latest Close Price
   * 30-Day ROC (%)
   * Color-coded for clarity

---

## ⚡ Customization

* Change the analysis period:

  ```python
  ROC_PERIOD = 30  # days
  ```
* Adjust number of top gainers/losers:

  ```python
  TOP_N = 10
  ```

---

## 📈 Sample Output

Example: *Top 10 Gainers vs Top 10 Losers - 30-Day ROC*

![Example Chart](./output/example_chart.png)

---

## 📜 License

MIT License. Free to use and modify.

````

---

## 🔹 Script Addition for Example Chart

In your script, after generating the **Top 10 Gainers vs Losers bar chart**, add:

```python
# Save example chart as PNG for README
plt.savefig(os.path.join(OUTPUT_DIR, "example_chart.png"))
````

👉 Place this **just before** `pdf.savefig()` in the bar chart section.

---

Would you like me to **inject this change into your full script** so you don’t have to place it manually?
