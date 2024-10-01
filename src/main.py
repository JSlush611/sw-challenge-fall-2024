from data_loader import DataLoader
from data_transformer import DataTransformer
from datetime import datetime
import os
import time

def main():
    print("Welcome to the CTG Data Processing Tool")

    # Get data directories from user
    raw_data_dir = input("Enter the path to the raw data directory (e.g., ../data/raw): ").strip()
    cleaned_data_dir = input("Enter the path to save cleaned data (e.g., ../data/cleaned): ").strip()

    # Check and create directories if necessary
    if not os.path.exists(raw_data_dir):
        print(f"Error: The raw data directory '{raw_data_dir}' does not exist.")

        return
    
    if not os.path.exists(cleaned_data_dir):
        print(f"Error: The cleaned data directory '{cleaned_data_dir}' does not exist. Creating it now.")
        os.makedirs(cleaned_data_dir)

    data_loader = DataLoader(raw_data_dir, cleaned_data_dir)

    start_time = time.time()  
    cleaned_data = data_loader.load_data()
    if not cleaned_data:
        print("No data loaded. Exiting.")

        return
    
    end_time = time.time()
    print(f"Data loading and cleaning completed in {end_time - start_time:.2f} seconds.")

    output_file = f"cleaned_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    data_loader.save_data_to_csv(output_file)
    print(f"Cleaned data successfully saved to '{output_file}'.")

    transformer = DataTransformer(cleaned_data)
    print("\nNext, let's configure the time range and interval for OHLCV data generation.")

    while True:
        start_time_str = input("Enter the start time (e.g., 2024-09-16 10:00:00): ").strip()
        end_time_str = input("Enter the end time (e.g., 2024-09-16 10:01:00): ").strip()

        try:
            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

            if start_time >= end_time:
                print("Error: Start time must be before end time. Please try again.")
            else:
                break

        except ValueError:
            print("Error: Invalid datetime format. Please enter the date and time in the format 'YYYY-MM-DD HH:MM:SS'.")

    # Validate interval input and generate OHLCV data
    while True:
        interval = input("Enter the time interval for OHLCV calculation (e.g., 15s, 1m, 1h): ").strip()
        try:
            transformer.parse_interval(interval)  

            break  

        except ValueError as e:
            print(f"Error: {e}. Please enter a valid time interval (e.g., '15s', '1m', '1h').")

    ohlcv_data = transformer.calculate_ohlcv(start_time, end_time, interval)
    if not ohlcv_data:
        print("No OHLCV data calculated. Exiting.")

        return

    print("\nSaving OHLCV data...")
    start_time_str = start_time.strftime('%Y%m%d_%H%M%S')
    end_time_str = end_time.strftime('%Y%m%d_%H%M%S')
    file_name = f"ohlcv_{start_time_str}_to_{end_time_str}_{interval}.csv"
    transformer.save_ohlcv_to_csv(ohlcv_data, start_time, end_time, interval, file_name)
    print(f"OHLCV data successfully saved to ", file_name)

if __name__ == "__main__":
    main()