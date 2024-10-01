from data_loader import DataLoader
from data_transofmer import DataTransformer
from datetime import datetime
import os

def main():
    print("Welcome to the CTG Data Processing Tool")

    raw_data_dir = input("Enter the path to the raw data directory (e.g., ../data/raw): ").strip()
    cleaned_data_dir = input("Enter the path to save cleaned data (e.g., ../data/cleaned): ").strip()

    if not os.path.exists(raw_data_dir):
        print(f"Error: The raw data directory '{raw_data_dir}' does not exist.")

        return
    
    if not os.path.exists(cleaned_data_dir):
        print(f"Error: The cleaned data directory '{cleaned_data_dir}' does not exist. Creating it now.")
        os.makedirs(cleaned_data_dir)

    data_loader = DataLoader(raw_data_dir, cleaned_data_dir)

    cleaned_data = data_loader.load_data()
    if not cleaned_data:
        print("No data loaded. Exiting.")

        return
    
    data_loader.save_data_to_csv("cleaned_data_output.csv")
    print("Cleaned data successfully saved to 'cleaned_data_output.csv'.")
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

    while True:
        interval = input("Enter the time interval for OHLCV calculation (e.g., 15s, 1m, 1h): ").strip()

        try:
            transformer.parse_interval(interval)  

            break  
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid time interval (e.g., '15s', '1m', '1h').")

    transformer = DataTransformer(cleaned_data)
    ohlcv_data = transformer.calculate_ohlcv(start_time, end_time, interval)
    if not ohlcv_data:
        print("No OHLCV data calculated. Exiting.")

        return

    print("\nSaving OHLCV data...")
    transformer.save_ohlcv_to_csv(ohlcv_data, start_time, end_time, interval)
    print("OHLCV data successfully saved.")

if __name__ == "__main__":
    main()