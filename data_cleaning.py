
import csv

def clean_row(header, row, irrelevant_columns):
    cleaned = []
    for column, cell in zip(header, row):
        if column not in irrelevant_columns:
            normalized_cell = cell.strip().replace('\u200b', '').replace('\ufeff', '')
            if normalized_cell.lower() in ['', 'n/a', 'nan', 'null', 'none', 'undefined', ""]:
                cleaned.append(None)  
            else:
                cleaned.append(normalized_cell)
    return cleaned

# Columns to remove
irrelevant_columns = [
    'scrape_id', 'last_scraped', 'source', 'neighborhood_overview',
    'picture_url', 'host_url', 'host_about', 'host_thumbnail_url',
    'host_picture_url', 'host_verifications', 'host_has_profile_pic',
    'neighbourhood_group_cleansed', 'bathrooms', 'bedrooms', 'amenities',
    'minimum_minimum_nights', 'maximum_minimum_nights', 'minimum_maximum_nights',
    'maximum_maximum_nights', 'minimum_nights_avg_ntm', 'maximum_nights_avg_ntm',
    'calendar_updated', 'has_availability', 'availability_30', 'availability_60',
    'availability_90', 'availability_365', 'calendar_last_scraped',
    'number_of_reviews_ltm', 'number_of_reviews_l30d', 'license'
]


try:
    with open('data/listings.csv', mode='r', encoding='utf-8') as f, \
         open('data/listings_clean.csv', mode='w', newline='', encoding='utf-8') as f_new:
        csv_reader = csv.reader(f)
        csv_writer = csv.writer(f_new)

        header = next(csv_reader)
        cleaned_header = [column for column in header if column not in irrelevant_columns]
        csv_writer.writerow(cleaned_header)

        for row in csv_reader:
            cleaned_row = clean_row(header, row, irrelevant_columns)
            csv_writer.writerow(cleaned_row)
except Exception as e:
    print(f"Error occurred: {e}")


import pandas as pd

data_clean = pd.read_csv('data/listings_clean.csv')

print("Empty strings remaining:", (data_clean == '').sum().sum())
print("Original 'N/A' strings converted:", (data_clean == 'N/A').sum().sum())
print(data_clean.sample(10))

print()
data_clean = pd.read_csv('data/listings_clean.csv')
sample_data = data_clean.head(20)
markdown_table = sample_data.to_markdown(index=False)
#print(markdown_table)









