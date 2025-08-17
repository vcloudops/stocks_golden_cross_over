import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import os

# Parameters
OUTPUT_DIR = "./output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NIFTY50_TICKERS = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS",
    "BEL.NS", "BHARTIARTL.NS", "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "EICHERMOT.NS", "ETERNAL.NS", "GRASIM.NS", "HCLTECH.NS",
    "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS", "INDUSINDBK.NS", "INFY.NS",
    "JSWSTEEL.NS", "JIOFIN.NS", "KOTAKBANK.NS", "LT.NS", "M&M.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS", "ONGC.NS", "POWERGRID.NS",
    "RELIANCE.NS", "SBILIFE.NS", "SHRIRAMFIN.NS", "SBIN.NS", "SUNPHARMA.NS", "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS",
    "TECHM.NS", "TITAN.NS", "TRENT.NS", "ULTRACEMCO.NS", "WIPRO.NS"
]
ROC_PERIOD = 30  # days for Rate of Change

# Function to calculate ROC
def calculate_roc(data, period=ROC_PERIOD):
    data["ROC"] = data["Close"].pct_change(periods=period) * 100
    return data

# Download all tickers at once
print("📥 Downloading data...")
all_data = yf.download(
    NIFTY50_TICKERS,
    period="1y",
    group_by="ticker",
    auto_adjust=False
)

results = []
for ticker in NIFTY50_TICKERS:
    try:
        if ticker not in all_data.columns.levels[0]:
            print(f"⚠️ No data for {ticker}")
            continue

        data = all_data[ticker].dropna().copy()
        if data.empty:
            print(f"⚠️ Empty dataset for {ticker}")
            continue

        data = calculate_roc(data)

        latest_roc = data["ROC"].dropna().iloc[-1] if not data["ROC"].dropna().empty else None
        latest_close = data["Close"].iloc[-1]

        results.append({
            "Ticker": ticker,
            "Latest Close": latest_close,
            f"{ROC_PERIOD}-Day ROC (%)": latest_roc,
            "Data": data
        })
    except Exception as e:
        print(f"❌ Error processing {ticker}: {e}")

# Create DataFrame summary
df = pd.DataFrame(results).drop(columns=["Data"])
df_sorted = df.sort_values(by=f"{ROC_PERIOD}-Day ROC (%)", ascending=False)

# Save CSV & Excel
df_sorted.to_csv(os.path.join(OUTPUT_DIR, "nifty_roc_summary.csv"), index=False)
df_sorted.to_excel(os.path.join(OUTPUT_DIR, "nifty_roc_summary.xlsx"), index=False)

# Date-stamped PDF filename
today_str = datetime.now().strftime("%Y-%m-%d")
pdf_filename = os.path.join(OUTPUT_DIR, f"nifty_roc_report_{today_str}.pdf")

# Create PDF Report
with PdfPages(pdf_filename) as pdf:
    # 1️⃣ Individual ROC Charts
    for r in results:
        plt.figure(figsize=(10, 5))
        plt.plot(r["Data"].index, r["Data"]["ROC"], label=f"{ROC_PERIOD}-Day ROC")
        plt.axhline(0, color="black", linestyle="--")
        plt.title(f"{r['Ticker']} - {ROC_PERIOD}-Day Rate of Change (ROC)")
        plt.xlabel("Date")
        plt.ylabel("ROC (%)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    # 2️⃣ Top 10 Gainers vs Top 10 Losers - Sorted Bar Chart
    top_gainers = df_sorted.head(10).copy()
    top_losers = df_sorted.tail(10).copy()

    # Mark groups
    top_gainers["Group"] = "Gainer"
    top_losers["Group"] = "Loser"

    comparison_df = pd.concat([top_gainers, top_losers])
    comparison_df = comparison_df.sort_values(by=f"{ROC_PERIOD}-Day ROC (%)", ascending=False)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        comparison_df["Ticker"],
        comparison_df[f"{ROC_PERIOD}-Day ROC (%)"],
        color=["green" if grp == "Gainer" else "red" for grp in comparison_df["Group"]]
    )

    # Annotate bars
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f"{height:.2f}",
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 5),
                     textcoords="offset points",
                     ha="center", va="bottom", fontsize=9)

    plt.title(f"Top 10 Gainers vs Top 10 Losers - {ROC_PERIOD}-Day ROC")
    plt.xlabel("Ticker")
    plt.ylabel("ROC (%)")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # ✅ Fix overlapping labels
    plt.xticks(rotation=45, ha="right", fontsize=9)

    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # 3️⃣ Summary Table
    summary_table = comparison_df.reset_index(drop=True)
    summary_display = summary_table[["Ticker", "Latest Close", f"{ROC_PERIOD}-Day ROC (%)"]].copy()
    summary_display["Latest Close"] = pd.to_numeric(summary_display["Latest Close"], errors="coerce").round(2)
    summary_display[f"{ROC_PERIOD}-Day ROC (%)"] = pd.to_numeric(
        summary_display[f"{ROC_PERIOD}-Day ROC (%)"], errors="coerce"
    ).round(2)

    if not summary_display.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.axis("off")

        # Row colors: green for gainers, red for losers
        cell_colors = []
        for grp in summary_table["Group"]:
            if grp == "Gainer":
                row_colors = ["palegreen"] * len(summary_display.columns)
            else:
                row_colors = ["lightcoral"] * len(summary_display.columns)
            cell_colors.append(row_colors)

        table = ax.table(
            cellText=summary_display.values,
            colLabels=summary_display.columns,
            cellColours=cell_colors,
            cellLoc="center",
            loc="center"
        )

        # ✅ Better readability for table
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.2)

        for key, cell in table.get_celld().items():
            cell.set_height(0.05)
            if key[0] == 0:  # header row
                cell.set_fontsize(10)
                cell.set_text_props(weight="bold")

        plt.title(f"Top 10 Gainers (Green) & Top 10 Losers (Red) - {ROC_PERIOD}-Day ROC", fontsize=12)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

print(f"✅ Report generated: {pdf_filename}, nifty_roc_summary.csv, nifty_roc_summary.xlsx")
