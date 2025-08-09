# Trader Behavior vs Market Sentiment Analysis

This project explores how trading behavior (profitability, risk, volume) aligns with or diverges from Bitcoin market sentiment (Fear/Greed).

## Structure

```
ds_abhishek/
├── notebook_1.ipynb          # Data loading, cleaning, feature engineering, EDA, visuals
├── notebook_2.ipynb          # Statistical tests, simple models, diagnostics
├── csv_files/                # Input datasets
│   ├── fear_greed_index.csv
│   └── historical_data.csv
├── outputs/                  # Saved charts and processed data
│   ├── figures/*.png
│   └── data/*.csv
├── ds_report.pdf             # Final report (to be generated)
└── requirements.txt          # Python dependencies
```

## Datasets
- `fear_greed_index.csv`: Columns `timestamp`, `value`, `classification`, `date`.
- `historical_data.csv`: Columns include `Account`, `Coin`, `Execution Price`, `Size Tokens`, `Size USD`, `Side`, `Timestamp IST`, `Start Position`, `Direction`, `Closed PnL`, `Fee`, etc.

## How to use
1. Create a virtual environment (recommended) and install dependencies:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Launch Jupyter and run `notebook_1.ipynb` first:
   ```bash
   jupyter lab
   ```
3. Run `notebook_2.ipynb` for statistical tests and simple modeling. Figures and processed datasets are saved under `outputs/`.

## Outputs
- Daily aggregates merged with sentiment
- Time-series and distribution plots (PNG)
- Basic correlations and simple models estimating relationships between sentiment and trading KPIs

## Notes
- The notebooks are robust to minor schema drift (e.g., missing leverage). Ensure date parsing for `Timestamp IST` uses the format `%d-%m-%Y %H:%M`.


