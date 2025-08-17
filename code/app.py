import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
from datetime import datetime

# Nifty 50 tickers with NSE suffix
NIFTY_50_TICKERS = [
    "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "TCS.NS",
    "LT.NS", "ITC.NS", "SBIN.NS", "AXISBANK.NS", "HINDUNILVR.NS",
    "BHARTIARTL.NS", "KOTAKBANK.NS", "BAJFINANCE.NS", "WIPRO.NS",
    "SUNPHARMA.NS", "ONGC.NS", "ADANIGREEN.NS", "ADANIPORTS.NS",
    "POWERGRID.NS", "NTPC.NS", "JSWSTEEL.NS", "TATASTEEL.NS",
    "HCLTECH.NS", "ULTRACEMCO.NS", "MARUTI.NS", "M&M.NS", "NESTLEIND.NS",
    "BRITANNIA.NS", "TECHM.NS", "CIPLA.NS", "DRREDDY.NS", "HEROMOTOCO.NS",
    "BAJAJFINSV.NS", "ASIANPAINT.NS", "HDFCLIFE.NS", "GRASIM.NS",
    "TITAN.NS", "COALINDIA.NS", "EICHERMOT.NS", "DIVISLAB.NS",
    "BAJAJ-AUTO.NS", "SHREECEM.NS", "HINDALCO.NS", "BPCL.NS",
    "SBILIFE.NS", "ADANIENT.NS", "TATAMOTORS.NS", "UPL.NS"
]

def check_golden_cross(ticker):
    """
    Check if stock is in Golden Cross (50DMA > 200DMA).
    Returns stock data and Golden Cross date.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        if hist.empty:
            return None, None

        hist["SMA50"] = hist["Close"].rolling(window=50).mean()
        hist["SMA200"] = hist["Close"].rolling(window=200).mean()

        cross_date = None
        hist_shifted = hist.shift(1)
        crosses = (hist["SMA50"] > hist["SMA200"]) & (hist_shifted["SMA50"] <= hist_shifted["SMA200"])
        if crosses.any():
            cross_date = crosses.idxmax()

        last = hist.iloc[-1]
        if pd.notna(last["SMA50"]) and pd.notna(last["SMA200"]) and last["SMA50"] > last["SMA200"]:
            return hist, cross_date
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
    return None, None


if __name__ == "__main__":
    results = []
    charts = []

    for ticker in NIFTY_50_TICKERS:
        hist, cross_date = check_golden_cross(ticker)
        if hist is not None:
            last = hist.iloc[-1]
            days_ago = (datetime.today() - cross_date.tz_localize(None)).days if cross_date else None
            results.append({
                "Ticker": ticker,
                "Last Price": round(last["Close"], 2),
                "SMA50": round(last["SMA50"], 2),
                "SMA200": round(last["SMA200"], 2),
                "Golden Cross Date": cross_date.date() if cross_date else None,
                "Days Since Golden Cross": days_ago
            })
            charts.append((ticker, hist, cross_date))

    df = pd.DataFrame(results)

    if df.empty:
        print("⚠️ No Nifty 50 stocks are above the Golden Cross right now.")
    else:
        print("✅ Nifty 50 Stocks Above Golden Cross:\n")
        print(df.to_string(index=False))

        # Save CSV with color coding for fresh crosses (<30 days)
        csv_file = "nifty50_golden_cross.csv"
        df.to_csv(csv_file, index=False)
        print(f"\n📁 Results saved to {csv_file}")

        try:
            import openpyxl
            excel_file = "nifty50_golden_cross.xlsx"
            with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Golden Cross")
                workbook = writer.book
                sheet = writer.sheets["Golden Cross"]

                # Color fresh crosses (<30 days) green
                for idx, days in enumerate(df["Days Since Golden Cross"], start=2):  # Excel rows start at 1 + header
                    if days is not None and days <= 30:
                        for col in range(1, len(df.columns)+1):
                            cell = sheet.cell(row=idx, column=col)
                            cell.fill = openpyxl.styles.PatternFill(start_color="C6EFCE",
                                                                    end_color="C6EFCE",
                                                                    fill_type="solid")
            print(f"🟢 Excel file with fresh crosses highlighted saved to {excel_file}")
        except ImportError:
            print("⚠️ openpyxl not installed. Install it to get Excel highlighting.")

        # Save charts to PDF with highlighted Golden Cross
        os.makedirs("charts", exist_ok=True)
        pdf_path = "charts/nifty50_golden_cross_report.pdf"
        with PdfPages(pdf_path) as pdf:
            for ticker, hist, cross_date in charts:
                plt.figure(figsize=(10,6))
                plt.plot(hist.index, hist["Close"], label="Close Price", color="black", linewidth=1)
                plt.plot(hist.index, hist["SMA50"], label="50 DMA", color="blue", linewidth=1.2)
                plt.plot(hist.index, hist["SMA200"], label="200 DMA", color="red", linewidth=1.2)

                if cross_date is not None:
                    price_on_cross = hist.loc[cross_date, "Close"]
                    plt.scatter(cross_date, price_on_cross, color="green", s=100, zorder=5)
                    plt.annotate(f"Golden Cross\n{cross_date.date()}",
                                 xy=(cross_date, price_on_cross),
                                 xytext=(cross_date, price_on_cross*1.05),
                                 arrowprops=dict(facecolor='green', shrink=0.05),
                                 fontsize=9, color="green")

                plt.title(f"{ticker} – Golden Cross")
                plt.xlabel("Date")
                plt.ylabel("Price (INR)")
                plt.legend()
                plt.grid(True, linestyle="--", alpha=0.6)
                plt.tight_layout()
                pdf.savefig()
                plt.close()
        print(f"🖼️ Charts PDF saved to {pdf_path}")