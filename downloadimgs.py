import json
import os
import requests
from urllib.parse import urlparse

# Load school data
with open('schools.json', 'r') as f:
    schools_data = json.loads(f.read())

# Create img directory if needed
os.makedirs('img', exist_ok=True)

for school in schools_data['schools']:
    original_url = school['logo']
    if not original_url:
        continue
    
    # Extract filename from URL
    url_path = urlparse(original_url).path
    filename = os.path.basename(url_path)
    
    # Get file extension from original URL
    ext = os.path.splitext(filename)[1]
    if not ext:
        # Default to jpg if no extension found
        ext = '.jpg'
        filename += ext
    
    local_path = f"img/{filename}"
    
    # Download and save image
    try:
        response = requests.get(original_url, timeout=10)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
        
        # Update JSON with local path
        school['logo'] = f"/{local_path}"
    except Exception as e:
        print(f"Failed to download {original_url}: {str(e)}")

# Save modified JSON
with open('schools.json', 'w') as f:
    f.write(json.dumps(schools_data, indent=2))

print("Image download and path update complete")
