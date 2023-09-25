import csv

# Create a dictionary with 'station_id' included
data = {
    'station_id': [254315075211501, 254530074280001, 251440075023001],
    'station_name': ['AMARWASI', 'BANERAMATAJI', 'BARASNI'],
    'latitude': [25.72083333, 25.4875, 25.75833333],
    'longitude': [75.35416667, 74.7, 74.46666667],
    '2010_1': [5.87, 16.72, 11.04],
    '2010_2': [8.05, None, 16.9],  # Replace 'None' with your data
    '2010_3': [2.35, 17.17, 15.48],
    '2010_4': [3.19, 16.53, 12.48]
}

# Define the output CSV file path
csv_file = 'output.csv'

# Write the dictionary to the CSV file
with open(csv_file, 'w', newline='') as csvfile:
    fieldnames = data.keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data
    for i in range(len(data['station_id'])):
        row = {field: data[field][i] for field in fieldnames}
        writer.writerow(row)

print(f'Data saved to {csv_file}')
