from flask import Flask, render_template_string
import pandas as pd
import os
import io
import base64
import calendar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load the BA stock data once at module import
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'ba.us.txt')

# Read CSV, drop OpenInt (if present), and prepare date-sliced DataFrames
_df = pd.read_csv(DATA_PATH)
# Drop OpenInt column to simplify downstream analysis
_df = _df.drop(columns=['OpenInt'], errors='ignore')
_df['Date'] = pd.to_datetime(_df['Date'])

# Split into three time-based DataFrames. Reasoning:
# - 1970-1989: early historical period capturing market behavior and long-term growth
# - 1990-1999: 1990s era (tech boom and different market dynamics)
# - 2000-2017: modern era including 2000s/2008 crisis and recovery up to dataset end (2017-11-10)
df_1970_1989 = _df[_df['Date'] <= '1989-12-31'].copy()
df_1990_1999 = _df[( _df['Date'] >= '1990-01-01') & (_df['Date'] <= '1999-12-31')].copy()
df_2000_2017 = _df[_df['Date'] >= '2000-01-01'].copy()

def _avg_monthly_volume_by_monthname(df):
    # group by calendar month and compute mean volume
    monthly = df.groupby(df['Date'].dt.month)['Volume'].mean()
    # ensure all months present (1..12)
    monthly = monthly.reindex(range(1,13), fill_value=0)
    # convert to month names for x-axis
    months = [calendar.month_abbr[i] for i in range(1,13)]
    return months, monthly.values

months, vals_70_89 = _avg_monthly_volume_by_monthname(df_1970_1989)
_, vals_90_99 = _avg_monthly_volume_by_monthname(df_1990_1999)
_, vals_00_17 = _avg_monthly_volume_by_monthname(df_2000_2017)

# Create a grouped bar chart and encode to base64 PNG for embedding
def _make_grouped_bar_png(months, a, b, c, labels=('1970-1989','1990-1999','2000-2017')):
    fig, ax = plt.subplots(figsize=(10,4))
    x = range(len(months))
    width = 0.25
    ax.bar([i - width for i in x], a, width=width, label=labels[0])
    ax.bar(x, b, width=width, label=labels[1])
    ax.bar([i + width for i in x], c, width=width, label=labels[2])
    ax.set_xticks(x)
    ax.set_xticklabels(months)
    ax.set_ylabel('Average Monthly Volume')
    ax.set_title('Average Monthly Volume by Calendar Month (three eras)')
    ax.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode('ascii')
    return data

_monthly_volume_chart_b64 = _make_grouped_bar_png(months, vals_70_89, vals_90_99, vals_00_17)

# --- 4th Commit: yearly moving average of Open price (line chart) ---
def _annual_open_and_ma(df, window=3):
    # group by year and compute mean Open price
    annual = df.groupby(df['Date'].dt.year)['Open'].mean().sort_index()
    # compute simple moving average over `window` years
    ma = annual.rolling(window=window, min_periods=1, center=False).mean()
    return annual.index.to_list(), annual.values, ma.values

years_70, annual_70, ma_70 = _annual_open_and_ma(df_1970_1989, window=3)
years_90, annual_90, ma_90 = _annual_open_and_ma(df_1990_1999, window=3)
years_00, annual_00, ma_00 = _annual_open_and_ma(df_2000_2017, window=3)

def _make_yearly_ma_line_png(series_list, labels_list, colors=None):
    fig, ax = plt.subplots(figsize=(10,4))
    for (years, annual, ma), label in zip(series_list, labels_list):
        # plot the moving average line
        ax.plot(years, ma, marker='o', label=label)
    ax.set_xlabel('Year')
    ax.set_ylabel('Open Price (USD) - 3yr MA')
    ax.set_title('Yearly Open Price (3-year moving average) by Era')
    ax.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode('ascii')
    return data

_yearly_open_ma_chart_b64 = _make_yearly_ma_line_png(
    [ (years_70, annual_70, ma_70), (years_90, annual_90, ma_90), (years_00, annual_00, ma_00) ],
    ['1970-1989 (3yr MA)','1990-1999 (3yr MA)','2000-2017 (3yr MA)']
)


# --- 5th Commit: yearly moving average of Close price (line chart) ---
def _annual_close_and_ma(df, window=3):
    annual = df.groupby(df['Date'].dt.year)['Close'].mean().sort_index()
    ma = annual.rolling(window=window, min_periods=1).mean()
    return annual.index.to_list(), annual.values, ma.values

years_c_70, annual_c_70, ma_c_70 = _annual_close_and_ma(df_1970_1989, window=3)
years_c_90, annual_c_90, ma_c_90 = _annual_close_and_ma(df_1990_1999, window=3)
years_c_00, annual_c_00, ma_c_00 = _annual_close_and_ma(df_2000_2017, window=3)

_yearly_close_ma_chart_b64 = _make_yearly_ma_line_png(
    [ (years_c_70, annual_c_70, ma_c_70), (years_c_90, annual_c_90, ma_c_90), (years_c_00, annual_c_00, ma_c_00) ],
    ['1970-1989 Close (3yr MA)','1990-1999 Close (3yr MA)','2000-2017 Close (3yr MA)']
)


@app.route('/')
def index():
    """Load and display BA stock data as HTML table"""
    df = _df
    html_table = df.to_html(classes='table table-striped', index=False)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>BA Stock Data - Boeing</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css">
        <style>
            body {{ padding: 20px; background-color: #f5f5f5; }}
            h1 {{ color: #333; margin-bottom: 20px; }}
            .table {{ background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📈 BA (The Boeing Company) - Historical Stock Data</h1>
            <p class="text-muted">Total records: {len(df)}</p>
            <h4>Average monthly volume (by calendar month)</h4>
            <p class="text-muted">Bar chart compares average monthly volume (Jan–Dec) across three eras.</p>
            <img src="data:image/png;base64,{_monthly_volume_chart_b64}" alt="avg monthly volume chart" style="max-width:100%;height:auto;"/>

            <h4 class="mt-4">Yearly Open price (3-year moving average)</h4>
            <p class="text-muted">Line chart shows the yearly open price smoothed with a 3-year moving average for each era.</p>
            <img src="data:image/png;base64,{_yearly_open_ma_chart_b64}" alt="yearly open ma chart" style="max-width:100%;height:auto;"/>

            <h4 class="mt-4">Yearly Close price (3-year moving average)</h4>
            <p class="text-muted">Line chart shows the yearly close price smoothed with a 3-year moving average for each era.</p>
            <img src="data:image/png;base64,{_yearly_close_ma_chart_b64}" alt="yearly close ma chart" style="max-width:100%;height:auto;"/>
            {html_table}
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)


@app.route('/api/data')
def api_data():
    """Return stock data as JSON"""
    return _df.to_json(orient='records')


@app.route('/api/summary')
def api_summary():
    """Return summary statistics"""
    df = _df
    summary = {
        'total_records': len(df),
        'date_range': f"{df['Date'].min().date()} to {df['Date'].max().date()}",
        'avg_close': float(df['Close'].mean()),
        'highest_close': float(df['Close'].max()),
        'lowest_close': float(df['Close'].min())
    }
    return summary


if __name__ == '__main__':
    app.run(debug=True, port=5000)
