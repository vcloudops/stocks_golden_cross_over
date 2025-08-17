
Here’s a **complete `README.md`** tailored for your Nifty 50 Golden Cross project with Docker support:

---

# Nifty 50 Golden Cross Tracker

This project identifies Nifty 50 stocks that are currently **above the golden cross** (50-day SMA crossing above 200-day SMA) and generates a report with CSV, Excel, and PDF charts.

---

## Features

* Pulls Nifty 50 stock data using **yfinance**
* Detects the **golden cross** for each stock
* Handles timezone-aware datetime issues and ensures enough historical data
* Generates outputs:

  * `CSV` with all results
  * `Excel` with recent crosses highlighted
  * `PDF` report with charts for each stock

---

## Prerequisites

* [Docker](https://www.docker.com/) installed
* Internet connection to fetch stock data

---

## Project Structure

```
.
├── Dockerfile
├── README.md
├── requirements.txt
├── robust_nifty_golden_cross.py
└── output/  # will be created automatically
```

---

## Usage

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

---

### 2️⃣ Build Docker image

```bash
docker build -t nifty-golden-cross .
```

---

### 3️⃣ Run the container

```bash
docker run --rm -v $(pwd)/output:/app/output nifty-golden-cross
```

* Output files will be saved in `./output`:

  * `nifty50_golden_cross.csv`
  * `nifty50_golden_cross.xlsx`
  * `nifty50_golden_cross_report.pdf`

> **Windows PowerShell:** use `${PWD}` instead of `$(pwd)`:

```powershell
docker run --rm -v ${PWD}/output:/app/output nifty-golden-cross
```

---

## Configuration

* **Tickers**: Modify the `NIFTY_50_TICKERS` list in `robust_nifty_golden_cross.py`
* **SMA periods**: Adjust `SMA_SHORT` and `SMA_LONG`
* **Highlight recent crosses**: Modify `RECENT_DAYS`

---

## Notes

* The script requires at least **200 trading days** of data for accurate SMA calculations
* Handles errors gracefully: missing or invalid tickers will be skipped
* Adjusts for **splits and dividends** using `auto_adjust=True` in yfinance

---

## License

MIT License

---