from flask import Flask, render_template_string
import pandas as pd
import os

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
