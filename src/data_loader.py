import os
import csv
import concurrent.futures
import logging
from data_cleaner import DataCleaner

logger = logging.getLogger('DataLoader')
logger.setLevel(logging.INFO)

if not logger.handlers:
    log_file = '../data/logs/loading/data_loader.log'
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file, mode='w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

class DataLoader:
    def __init__(self, data_dir, output_dir):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.data = []
        self.logger = logger  

    def get_file_list(self):
        """Get list of all CSV files in the data directory, sorted by filename."""
        try:
            files = [file for file in os.listdir(self.data_dir) if file.endswith('.csv')]
            files.sort()

            self.logger.info(f"Found {len(files)} CSV files in directory {self.data_dir}.")

            return files
        except Exception as e:
            self.logger.error(f"Error accessing directory {self.data_dir}: {e}")

            return []

    def _load_and_clean_file(self, file):
        """Helper function to load and clean a single file."""
        file_path = os.path.join(self.data_dir, file)
        raw_data = []

        try:
            with open(file_path, mode='r') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    raw_data.append(row)

            self.logger.info(f"Loaded {len(raw_data)} rows from {file}.")
        except Exception as e:
            self.logger.error(f"Error loading file {file}: {e}")
            
            return []

        cleaner = DataCleaner(raw_data)
        cleaned_data = cleaner.clean_data()

        self.logger.info(f"Cleaned data from {file}: {len(cleaned_data)} valid rows.")

        return cleaned_data

    def load_data(self):
        """Load and concatenate all data files into a single cleaned dataset."""
        self.logger.info("Starting to load and clean data.")

        files = self.get_file_list()
        if not files:
            self.logger.error("No files found to process.")

            return self.data

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self._load_and_clean_file, files)

        for result in results:
            self.data.extend(result)

        self.logger.info(f"Finished loading and cleaning data. Total valid rows: {len(self.data)}.")

        return self.data

    def save_data_to_csv(self, file_name):
        """Save the combined cleaned data to a CSV file."""
        if not self.data:
            self.logger.warning("No data to write to CSV.")

            return

        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)

                self.logger.info(f"Created output directory: {self.output_dir}.")
            except OSError as e:
                self.logger.error(f"Error creating directory {self.output_dir}: {e}")

                return

        fieldnames = self.data[0].keys()
        output_file = os.path.join(self.output_dir, file_name)

        try:
            with open(output_file, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.data)

            self.logger.info(f"Data successfully written to {output_file}.")
        except Exception as e:
            self.logger.error(f"Error writing to {output_file}: {e}")