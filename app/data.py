from flask import Flask, render_template_string
import pandas as pd
import os

app = Flask(__name__)

# Load the BA stock data
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'ba.us.txt')

@app.route('/')
def index():
    """Load and display BA stock data as HTML table"""
    df = pd.read_csv(DATA_PATH)
    html_table = df.to_html(classes='table table-striped')
    
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
    df = pd.read_csv(DATA_PATH)
    return df.to_json(orient='records')

@app.route('/api/summary')
def api_summary():
    """Return summary statistics"""
    df = pd.read_csv(DATA_PATH)
    summary = {
        'total_records': len(df),
        'date_range': f"{df['Date'].min()} to {df['Date'].max()}",
        'avg_close': float(df['Close'].mean()),
        'highest_close': float(df['Close'].max()),
        'lowest_close': float(df['Close'].min())
    }
    return summary

if __name__ == '__main__':
    app.run(debug=True, port=5000)
