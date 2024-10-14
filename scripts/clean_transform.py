import pandas as pd
import os

def clean_data(file_path):
    # Load data
    data = pd.read_csv(file_path)

    # Remove duplicates
    data.drop_duplicates(inplace=True)

    # Handle missing values
    data['message'].fillna('', inplace=True)

    # Validate data
    data['date'] = pd.to_datetime(data['date'], errors='coerce')


    # Remove rows with invalid dates
    data.dropna(subset=['date'], inplace=True)

    return data

if __name__ == '__main__':
    input_dir = '../scraping/data/raw'
    output_dir = './data/cleaned_transformed'
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_dir, filename)
            cleaned_data = clean_data(file_path)
            cleaned_file_path = os.path.join(output_dir, filename)
            cleaned_data.to_csv(cleaned_file_path, index=False)
            print(f'Cleaned data saved to {cleaned_file_path}')
