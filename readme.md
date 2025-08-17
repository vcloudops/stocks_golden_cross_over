# 📈 Nifty 50 Golden Cross Tracker

This project pulls Nifty 50 stock data, identifies stocks **above the Golden Cross** (50-day SMA crossing above 200-day SMA), and generates CSV, Excel, and PDF charts. It runs fully inside a **Docker container**, so no local Python setup is required.

## 🛠 Features

* Detects **Golden Cross** for Nifty 50 stocks.
* Outputs a **CSV** with:

  * Ticker
  * Last price
  * 50 SMA, 200 SMA
  * Golden Cross date
  * Days since Golden Cross
* Optional **Excel** file with **highlighted recent crosses** (<30 days).
* Generates **PDF charts** with Golden Cross marked.
* Fully portable via **Docker container**.

---

## 📦 Requirements

* Docker installed
* Internet access (to pull stock data via Yahoo Finance)

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/nifty-golden-cross.git
cd nifty-golden-cross
```

### 2. Build Docker image

```bash
docker build -t nifty-golden-cross .
```

### 3. Run the container

```bash
docker run --rm -v $(pwd)/output:/app/output nifty-golden-cross
```

* `-v $(pwd)/output:/app/output` mounts a local folder for saving CSV, Excel, and PDF files.

### 4. Output

After running, check the `output` folder for:

* `nifty50_golden_cross.csv` – Golden Cross stocks
* `nifty50_golden_cross.xlsx` – Excel with recent crosses highlighted
* `charts/nifty50_golden_cross_report.pdf` – PDF charts

---

## 📝 Notes

* If no stocks are above the Golden Cross, the script prints a warning and exits.
* Excel highlighting requires `openpyxl`. It's included in the Docker image.
* PDF charts are generated using `matplotlib`. No GUI is required (backend is set to `Agg`).

---

## 📌 Customization

* Modify the `NIFTY_50_TICKERS` list in `nifty_golden_cross_report_color.py` to add/remove stocks.
* Change the **fresh cross period** by adjusting:

```python
if days is not None and days <= 30:
```

* Adjust PDF chart styles inside the script if needed.

---

## 🐳 Docker Notes

* Works on Linux, Mac, and Windows with Docker Desktop.
* No local Python installation required.
* To update libraries, rebuild the Docker image with:

```bash
docker build --no-cache -t nifty-golden-cross .
```

---

## 📊 Sample Output

### CSV Output

| Ticker      | Last Price | SMA50   | SMA200  | Golden Cross Date | Days Since Golden Cross |
| ----------- | ---------- | ------- | ------- | ----------------- | ----------------------- |
| RELIANCE.NS | 2450.50    | 2430.20 | 2380.75 | 2025-07-10        | 38                      |
| HDFCBANK.NS | 1750.30    | 1735.10 | 1700.60 | 2025-07-15        | 33                      |

*Example CSV screenshot:*
![CSV Screenshot](screenshots/csv_example.png)

---

### Excel Output

* Recent Golden Crosses (<30 days) are highlighted in **green**.

*Example Excel screenshot:*
![Excel Screenshot](screenshots/excel_example.png)

---

### PDF Charts

* Each chart shows **Close price**, **50 DMA**, **200 DMA**, and **Golden Cross date**.

*Example PDF chart screenshot:*
![PDF Chart Screenshot](screenshots/pdf_chart_example.png)

---

### Optional Next Step

You can automate **daily runs** using a cron job or CI/CD pipeline to always have the latest Golden Cross data.

---

If you want, I can **also create a folder structure** with `screenshots/` placeholders and a ready-to-use Docker output folder so your README images work immediately.

Do you want me to do that?
