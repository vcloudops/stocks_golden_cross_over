---

# Nifty 50 Return of Change Tracker

This project analyzes the **NIFTY50 stocks** using **Rate of Change (ROC)** over the last 30 days, identifies the **top gainers** and **top losers**, and generates reports in  CSV, Excel, and PDF formats

---

## 🚀 Features
* Fetches **1 year of historical stock data** for all NIFTY50 tickers from **yfinance**
* Calculates **30-day ROC (%)** for each stock.
* Identifies **Top N Gainers** and **Top N Losers** (default: 10).
* Generates output files:

  * **CSV** with all results
  * **Excel** with recent crosses highlighted
  * **PDF** report with charts for each stock

---

## Prerequisites

* [Docker](https://www.docker.com/) installed
* yfinance api connection to fetch stock data

---

## Project Structure

```
.
├── Dockerfile
├── README.md
├── requirements.txt
├── app.py
└── output/  # created automatically when running
```

---

## Usage

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>/Nifty50ReturnofChangeTracker/code
```

---

### 2️⃣ Build Docker image

```bash
docker build -t nifty-roc .
```

---

### 3️⃣ Run the container

```bash
docker run --rm -v $(pwd)/output:/app/output nifty-roc
```

* Output files will be saved in `./output`:

  * `nifty_roc_summary.csv`
  * `nifty_roc_summary.xlsx`
  * `nifty_roc_report_YYYY-MM-DD.pdf`

> **Windows PowerShell:** use `${PWD}` instead of `$(pwd)`:

```powershell
docker run --rm -v $(pwd)/output:/app/output nifty-roc
```

---

## Configuration

* **Tickers**: Modify the `NIFTY_50_TICKERS` list in `app.py`
* **SMA periods**: Adjust `ROC_PERIOD`
* **Adjust number of top gainers/losers**:

  ```python
  TOP_N = 10
  ```
## License

MIT License

---