import os
from datetime import datetime

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


BASE_DIR = "/Users/kumarabhishek/Desktop/Assignment_task/ds_abhishek"
OUT_DATA = os.path.join(BASE_DIR, "outputs", "data")
OUT_FIG = os.path.join(BASE_DIR, "outputs", "figures")
REPORT_PATH = os.path.join(BASE_DIR, "ds_report.pdf")


def draw_wrapped_text(c: canvas.Canvas, text: str, x: float, y: float, max_width: float, leading: float = 14):
    """Simple word-wrap for ReportLab canvas.drawString."""
    words = text.split()
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if c.stringWidth(test) <= max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= leading
            line = word
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def add_image(c: canvas.Canvas, img_path: str, x: float, y: float, max_width: float) -> float:
    if not os.path.exists(img_path):
        return y
    try:
        img = ImageReader(img_path)
        iw, ih = img.getSize()
        scale = min(max_width / iw, 1.0)
        w = iw * scale
        h = ih * scale
        # If not enough space on page, create a new page
        if y - h < 2 * cm:
            c.showPage()
            y = A4[1] - 2 * cm
        c.drawImage(img, x, y - h, width=w, height=h, preserveAspectRatio=True, anchor='nw')
        y -= (h + 0.5 * cm)
        return y
    except Exception:
        return y


def main():
    c = canvas.Canvas(REPORT_PATH, pagesize=A4)
    width, height = A4
    margin = 2 * cm
    x = margin
    y = height - margin

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x, y, "Trader Behavior vs Market Sentiment")
    y -= 22
    c.setFont("Helvetica", 11)
    y = draw_wrapped_text(c, "Analysis of trading KPIs aligned against Bitcoin Fear & Greed Index.", x, y, width - 2 * margin)

    # Load data and basic KPIs
    merged_path = os.path.join(OUT_DATA, "daily_metrics_with_sentiment.csv")
    if os.path.exists(merged_path):
        df = pd.read_csv(merged_path, parse_dates=["date"]) 
        df = df.sort_values("date")
        n_days = len(df)
        d0 = df["date"].min()
        d1 = df["date"].max()
        mean_fg = df["fg_value"].mean(skipna=True)
        total_volume = df["total_volume_usd"].sum(skipna=True)
        total_net_pnl = df["total_net_pnl_usd"].sum(skipna=True)
        rho = df[["fg_value", "total_net_pnl_usd"]].corr(method="spearman").iloc[0, 1]

        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y, "Summary")
        y -= 16
        c.setFont("Helvetica", 11)
        lines = [
            f"Date range: {d0.date() if pd.notna(d0) else 'NA'} to {d1.date() if pd.notna(d1) else 'NA'} ({n_days} days)",
            f"Average Fear & Greed value: {mean_fg:.2f}",
            f"Total traded volume (USD): {total_volume:,.0f}",
            f"Total net PnL (USD): {total_net_pnl:,.0f}",
            f"Spearman corr(FG, Net PnL): {rho:.3f}",
        ]
        for line in lines:
            c.drawString(x, y, line)
            y -= 14
        y -= 6
    else:
        c.setFont("Helvetica", 11)
        y = draw_wrapped_text(c, "Processed dataset not found. Please run notebook_1.ipynb to generate merged metrics.", x, y, width - 2 * margin)

    # Figures
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "Figures")
    y -= 16

    figures = [
        ("Daily Volume vs Fear & Greed Index", os.path.join(OUT_FIG, "timeseries_volume_vs_fg.png")),
        ("Daily Net PnL by Sentiment Classification", os.path.join(OUT_FIG, "boxplot_netpnl_by_classification.png")),
        ("FG Value vs Daily Net PnL", os.path.join(OUT_FIG, "scatter_fg_vs_netpnl.png")),
        ("Spearman Correlations", os.path.join(OUT_FIG, "corr_heatmap.png")),
    ]

    for title, path in figures:
        c.setFont("Helvetica", 11)
        y = draw_wrapped_text(c, title, x, y, width - 2 * margin)
        y = add_image(c, path, x, y, max_width=width - 2 * margin)

    # Footer
    c.setFont("Helvetica", 9)
    c.drawString(margin, 1.2 * cm, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.showPage()
    c.save()


if __name__ == "__main__":
    main()
