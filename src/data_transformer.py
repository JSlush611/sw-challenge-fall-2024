import os
import csv
from datetime import datetime, timedelta
from util import setup_logger

logger = setup_logger('DataTransformer', '../data/logs/transforming/data_transformer.log')

class DataTransformer:
    def __init__(self, data=None):
        self.data = data if data else []
        self.logger = logger  

    def set_data(self, new_data):
        """Set new data for transformation."""
        self.data = new_data
        self.logger.info(f"New data set with {len(new_data)} rows for transformation.")

    def parse_interval(self, interval):
        """Convert interval string to timedelta object."""
        time_units = {'d': 0, 'h': 0, 'm': 0, 's': 0}
        current_value = ''

        for char in interval:
            if char.isdigit():
                current_value += char

            elif char in time_units:
                if current_value:
                    time_units[char] = int(current_value)
                    current_value = ''
                else:
                    raise ValueError(f"Invalid interval format: {interval}")
                
            else:
                raise ValueError(f"Invalid character '{char}' in interval: {interval}")
            
        if current_value:
            raise ValueError(f"Invalid interval format: {interval}")

        self.logger.info(f"Parsed interval '{interval}' to timedelta: {time_units}.")
        return timedelta(
            days=time_units['d'],
            hours=time_units['h'],
            minutes=time_units['m'],
            seconds=time_units['s']
        )

    def filter_data_by_time_frame(self, start_time, end_time):
        """Filter data within the given time frame."""
        filtered_data = [
            row for row in self.data
            if start_time <= datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S.%f') < end_time
        ]
        
        self.logger.info(
            f"Filtered data from {start_time} to {end_time}. "
            f"Rows after filtering: {len(filtered_data)}."
        )

        return filtered_data

    def calculate_ohlcv(self, start_time, end_time, interval):
        """Calculate OHLCV bars for the given time frame and interval."""
        filtered_data = self.filter_data_by_time_frame(start_time, end_time)
        ohlcv_data = []
        current_interval_start = start_time
        interval_delta = self.parse_interval(interval)

        # User iter to avoid storing in extra lists
        filtered_data_iter = iter(filtered_data)
        try:
            row = next(filtered_data_iter)
        except StopIteration:
            row = None

        # For the start to end time we want to calculate the info for each interval
        while current_interval_start < end_time:
            current_interval_end = current_interval_start + interval_delta
            interval_rows = []

            # While the iter has another row in the range, add to interval rows
            while row and current_interval_start <= datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S.%f') < current_interval_end:
                interval_rows.append(row)
                try:
                    row = next(filtered_data_iter)
                except StopIteration:
                    row = None

            if interval_rows:
                open_price = interval_rows[0]['Price']
                high_price = max(r['Price'] for r in interval_rows)
                low_price = min(r['Price'] for r in interval_rows)
                close_price = interval_rows[-1]['Price']
                volume = sum(float(r['Size']) for r in interval_rows)

                ohlcv_data.append({
                    'Timestamp': current_interval_start.strftime('%Y-%m-%d %H:%M:%S'),
                    'Open': open_price,
                    'High': high_price,
                    'Low': low_price,
                    'Close': close_price,
                    'Volume': volume
                })

                self.logger.info(
                    f"OHLCV data calculated for interval starting at {current_interval_start}."
                )

            current_interval_start = current_interval_end

        self.logger.info(f"OHLCV calculation complete. Total intervals: {len(ohlcv_data)}.")
        
        return ohlcv_data

    def save_ohlcv_to_csv(self, ohlcv_data, start_time, end_time, interval, filename, output_dir='../data/ohlcv'):
        """Save OHLCV data to a CSV file."""
        os.makedirs(output_dir, exist_ok=True)

        file_path = os.path.join(output_dir, filename)

        try:
            with open(file_path, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=ohlcv_data[0].keys())
                writer.writeheader()
                writer.writerows(ohlcv_data)

            self.logger.info(f"OHLCV data successfully saved to {file_path}.")

        except Exception as e:
            self.logger.error(f"Error writing OHLCV data to CSV: {e}")