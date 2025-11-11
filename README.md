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

For the second commit I kept the Flask API behavior unchanged but cleaned and prepared the dataset for analysis:

- Dropped the `OpenInt` column from the loaded CSV to simplify the table and downstream metrics.
- Converted `Date` to datetime and split the original DataFrame (1970-01-02 through 2017-11-10) into three time-sliced DataFrames for focused analysis:
	- `df_1970_1989` — early historical period (1970-01-01 through 1989-12-31)
	- `df_1990_1999` — 1990s era (1990-01-01 through 1999-12-31)
	- `df_2000_2017` — modern era (2000-01-01 through dataset end 2017-11-10)

Reasoning: these splits provide natural historical groupings (early long-term growth, 1990s market dynamics, and the 2000s/2010s including the 2008 crisis and recovery) which can be useful for era-based analysis and modeling while keeping the API endpoints unchanged.


### 3rd Commit

### 4th Commit

### 5th Commit