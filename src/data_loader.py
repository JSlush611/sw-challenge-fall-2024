import os
import csv
import concurrent.futures
from data_cleaner import DataCleaner

# Negative, missing prices, outlier prices (41.xx), duplicate timestamps
class DataLoader:
    def __init__(self, data_dir, output_dir):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.data = []

    def get_file_list(self):
        """Get list of all CSV files in the data directory, sorted by filename."""
        files = [file for file in os.listdir(self.data_dir) if file.endswith('.csv')]
        
        return sorted(files)

    def _load_and_clean_file(self, file):
        """Helper function to load and clean a single file."""
        file_path = os.path.join(self.data_dir, file)
        raw_data = []

        try:
            with open(file_path, mode='r') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    raw_data.append(row)

        except Exception as e:
            print(f"Error loading {file}: {e}")
        
        cleaner = DataCleaner(raw_data, 400, 500)
        cleaned_data = cleaner.clean_data()
        
        return cleaned_data

    def load_data(self):
        """Load and concatenate all data files into a single cleaned dataset using multithreading."""
        files = self.get_file_list()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self._load_and_clean_file, files)

        for result in results:
            self.data.extend(result)

        return self.data

    def save_data_to_csv(self, file_name):
        """Save the combined cleaned data to a CSV file."""
        if not self.data:
            print("No data to write.")

            return

        fieldnames = self.data[0].keys()
        output_file = os.path.join(self.output_dir, file_name)

        try:
            with open(output_file, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.data)

            print(f"Data successfully written to {output_file}")

        except Exception as e:
            print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    loader = DataLoader('../data/raw', '../data/cleaned')
    cleaned_data = loader.load_data()

    print(f"Loaded and cleaned {len(cleaned_data)} rows.")
    loader.save_data_to_csv('cleaned_combied_data.csv')