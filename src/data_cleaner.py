import os
from util import setup_logger

logger = setup_logger('DataCleaner', '../data/logs/cleaning/data_cleaning.log')

if not logger.handlers:
    log_file = '../data/logs/cleaning/data_cleaning.log'
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file, mode='w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

class DataCleaner:
    def __init__(self, data=None, min_valid_price=400, max_valid_price=500):
        self.data = data if data else []
        self.min_valid_price = min_valid_price
        self.max_valid_price = max_valid_price
        self.logger = logger

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

                # Convert 'Price' to float and check validity
                price = float(row['Price'])
                if price <= 0:
                    self.logger.info(f"Removed due to non-positive price: {row}")

                    continue

                if price < self.min_valid_price or price > self.max_valid_price:
                    self.logger.info(f"Removed due to outlier price: {row}")

                    continue

                # Check for duplicate timestamps
                if row['Timestamp'] in seen_timestamps:
                    self.logger.info(f"Removed due to duplicate timestamp: {row}")

                    continue

                seen_timestamps.add(row['Timestamp'])
                cleaned_data.append(row)

            except ValueError as e:
                # Log any issues with value conversion
                self.logger.error(f"ValueError: {e} - Removed row: {row}")

                continue

        self.data = cleaned_data
        self.logger.info(f"Data cleaning complete. Total valid rows: {len(self.data)}.")

        return self.data