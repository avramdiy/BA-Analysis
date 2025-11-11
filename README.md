# TRG Week 49

## $BA (The Boeing Company)

- A NYSE-listed aerospace and defense company based in Chicago, Illinois (founded 1916). Boeing designs, manufactures, and services aircraft, satellites, and defense systems for commercial, military, and government customers worldwide. The company is one of the largest aerospace manufacturers and a major defense contractor, serving markets including commercial airlines, defense departments, and space exploration.

- https://www.kaggle.com/borismarjanovic/datasets

### 1st Commit

Created a Flask API (`app/data.py`) that loads BA stock historical data from `ba.us.txt` and displays it as an HTML dataframe with Bootstrap styling. The API includes three endpoints:
- **GET `/`**: Renders BA stock data as an interactive HTML table (12,076+ records from 1970-present)
- **GET `/api/data`**: Returns stock data as JSON format
- **GET `/api/summary`**: Returns summary statistics (record count, date range, average/highest/lowest close prices)

Run with: `python app/data.py` then visit `http://localhost:5000`

### 2nd Commit

### 3rd Commit

### 4th Commit

### 5th Commit