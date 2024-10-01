# CTG Data Processing Tool

## 📋 Project Overview
This tool processes high-frequency tick data for the fictional stock "CTG". It loads, cleans, and transforms the tick data into Open-High-Low-Close-Volume (OHLCV) bars for specified time intervals. This is essential for time series analysis, technical analysis, and quantitative trading strategies.

The tool is designed to handle large datasets efficiently and includes multithreading to speed up the data loading process. The project does not rely on any external Python libraries and adheres to Python’s built-in modules.

## 🚀 Features
- **Data Loading**: Loads multiple CSV files containing tick data.
- **Data Cleaning**: Automatically detects and resolves issues such as:
  - Missing or invalid `Price` or `Size` fields.
  - Outlier prices (defined by user-specified thresholds).
  - Duplicate timestamps.
- **Data Transformation**: Converts tick data into OHLCV bars based on user-specified time intervals and ranges.

## 🏁 Getting Started

### 1. **Clone the repository**:
Clone the repository to your local machine using SSH:
```bash
git clone git@github.com:<your-username>/sw-challenge-fall-2024.git
```
### 2. **Prepare the dataset**:
Ensure the raw data files (CSV format) are stored in a directory (e.g., ../data/raw). The directory should contain CSV files with tick data.

### 3. **Run the program**:
The program will interactively prompt you to enter the paths to your raw data directory, a directory to save the cleaned data, and the time range and interval for OHLCV generation.
```bash
python3 src/main.py
```

**Sample Input/Output Interaction**:
Welcome to the CTG Data Processing Tool
Enter the path to the raw data directory (e.g., ../data/raw): ../data/raw
Enter the path to save cleaned data (e.g., ../data/cleaned): ../data/cleaned
Data loading and cleaning completed in 3.91 seconds.
Cleaned data successfully saved to 'cleaned_data_20241001_102259.csv'.

Next, let's configure the time range and interval for OHLCV data generation.
Enter the start time (e.g., 2024-09-16 10:00:00): 2024-09-16 10:00:00
Enter the end time (e.g., 2024-09-16 10:01:00): 2024-09-16 10:01:00
Enter the time interval for OHLCV calculation (e.g., 15s, 1m, 1h): 15s
OHLCV data successfully saved to 'ohlcv_20240916_100000_to_20240916_100100_15s.csv'.


**Project Structure**:
.
├── data
│   ├── logs                  # Directory for storing log files
│   ├── raw                   # Directory for raw tick data (input)
│   ├── cleaned               # Directory for cleaned data (output)
│   ├── ohlcv                 # Directory for OHLCV output (output)
├── src
│   ├── main.py               # Main script to run the program
│   ├── data_loader.py        # Handles data loading and file management
│   ├── data_cleaner.py       # Cleans the raw tick data
│   ├── data_transformer.py   # Transforms cleaned tick data into OHLCV bars
│   ├── util.py               # Utility functions, including logging setup
└── README.md                 # This file

**Usage Guide**:
1. Data Loading: The tool will prompt you to enter the path to the directory where your raw CSV files are stored. Each file is loaded, and data cleaning is applied before storing the cleaned data.

2. Data Cleaning: During the data cleaning phase, the following issues are addressed:
    - Missing values in Price or Size.
    - Non-positive or outlier prices (based on defined thresholds).
    - Duplicate timestamps.

3. Data Transformation (OHLCV): You will specify a start time, end time, and a time interval (e.g., "15s", "1m"). The tool will generate OHLCV bars for the specified time range across the intervals and save the output as a CSV file.

**Assumptions and Limitations**:
Time Format: Timestamps in the data must be in the format YYYY-MM-DD HH:MM:SS.ssssss.

Data Consistency: It is assumed that the raw data is well-formed, with consistent timestamp formats.

File Structure: CSV files should have the following fields: Timestamp, Price, Size.

Performance Considerations: The tool is optimized for performance using multithreading and chunked writing, but performance may vary depending on system resources and dataset size.