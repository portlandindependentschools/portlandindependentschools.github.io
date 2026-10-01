import csv
import requests
import os
import re
from urllib.parse import urlparse

def sanitize_filename(name):
    sanitized = re.sub(r'[^a-zA-Z0-9]+', '-', name).lower()
    sanitized = sanitized.strip('-')
    return sanitized

def is_published(school):
    return (school.get('Publish') or '').strip().lower() == 'yes'

def extract_drive_file_id(url):
    """Extract the file ID from Google Drive URLs such as:
    https://drive.google.com/open?id=<id>
    https://drive.google.com/file/d/<id>/view?usp=sharing
    https://drive.google.com/uc?id=<id>&export=download
    """
    match = re.search(r'/d/([\w-]+)', url) or re.search(r'[?&]id=([\w-]+)', url)
    return match.group(1) if match else None

def download_logos():
    # Fetch CSV data from URL
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS5DPiVrMEHIFMWWZLUcmy4plA_RQ0gIJmG98PHUJ1LEdzobsfYoaf1io5GC2wP64im0qGG6AS8IBJl/pub?gid=1797278409&single=true&output=csv'
    response = requests.get(url)
    response.raise_for_status()

    csv_reader = csv.DictReader(response.text.splitlines())
    schools = [s for s in csv_reader if is_published(s)]

    os.makedirs('img', exist_ok=True)

    for school in schools:
        logo_url = school['Logo']
        if 'drive.google.com' not in logo_url:
            continue

        # Extract file ID from URL
        file_id = extract_drive_file_id(logo_url)
        if not file_id:
            print(f"Skipping invalid Google Drive URL: {logo_url}")
            continue
        thumbnail_url = f"https://drive.google.com/thumbnail?id={file_id}&sz=w800"

        # Sanitize school name for filename
        sanitized_name = sanitize_filename(school['Name'])
        filename = f"img/{sanitized_name}.jpg"

        # Skip if file already exists
        if os.path.exists(filename):
            print(f"Skipping existing file: {filename}")
            continue

        # Download the image
        try:
            response = requests.get(thumbnail_url, stream=True)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded {filename}")
        except Exception as e:
            print(f"Failed to download {thumbnail_url}: {e}")

if __name__ == '__main__':
    download_logos()
