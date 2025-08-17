---

# Nifty 50 Golden Cross Tracker

This project identifies **Nifty 50 stocks that are currently above the golden cross** (50-day SMA crossing above 200-day SMA) and generates reports in CSV, Excel, and PDF formats.

---

## Features

* Pulls Nifty 50 stock data using **yfinance**
* Detects the **golden cross** for each stock
* Handles timezone-aware datetime issues and ensures enough historical data
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
cd <repo-folder>/code
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

* The script requires at least **200 trading days** of historical data for accurate SMA calculations
* Handles errors gracefully: missing or invalid tickers will be skipped
* Uses **adjusted prices** (`auto_adjust=True`) for splits and dividends

---

## License

MIT License

---

This README now matches the Docker setup, script, and output workflow.

Do you want me to also create a **full zipped folder structure** ready for Docker build and run?
