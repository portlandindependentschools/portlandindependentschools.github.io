import json
import csv

# Load JSON data
with open('schools.json', 'r') as f:
    data = json.load(f)

# Create CSV file
with open('schools.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    
    # Write header
    writer.writerow(['Name', 'Description', 'Logo', 'Website'])
    
    # Write school data
    for school in data['schools']:
        writer.writerow([
            school['name'],
            school['description'],
            school['logo'],
            school['website']
        ])

print("Conversion complete. CSV file created successfully.")
