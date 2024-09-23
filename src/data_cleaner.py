import os
import csv
from datetime import datetime
import logging

class DataCleaner:
    def __init__(self, data=None, min_valid_price=400, max_valid_price=500, log_file='../data/logs/data_cleaning.log'):
        self.data = data if data else []
        self.min_valid_price = min_valid_price
        self.max_valid_price = max_valid_price

        logging.basicConfig(filename=log_file, 
                            level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filemode='w')
        self.logger = logging.getLogger()

    def set_data(self, new_data):
        """Reset the raw data with new data for cleaning."""
        self.data = new_data

    def clean_data(self):
        """Apply all cleaning steps in a single pass and log issues found."""
        seen_timestamps = set()
        cleaned_data = []

        for row in self.data:
            try:
                # Check for missing values in 'Price' and 'Size' fields
                if not row['Price'] or not row['Size']:
                    self.logger.info(f"Removed due to missing values: {row}")
                    continue

                # Convert 'Price' to float once and check for negatives or outliers 
                price = float(row['Price'])
                if price <= 0:
                    self.logger.info(f"Removed due to negative or zero price: {row}")
                    continue

                if price < self.min_valid_price or price > self.max_valid_price:
                    self.logger.info(f"Removed due to outlier price: {row}")
                    continue

                # Check for duplicate timestamps
                if row['Timestamp'] in seen_timestamps:
                    self.logger.info(f"Removed due to duplicate timestamp: {row}")
                    continue

                seen_timestamps.add(row['Timestamp'])

                # Append the cleaned row to the cleaned_data list
                cleaned_data.append(row)

            except ValueError:
                # Handle any conversion errors (e.g., invalid float conversion)
                self.logger.error(f"Removed due to ValueError: {row}")
                continue

        # Set the cleaned data back to the class attribute
        self.data = cleaned_data

        return self.data
