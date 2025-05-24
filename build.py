import csv
import requests
import os
import re
import json

def sanitize_filename(name):
    sanitized = re.sub(r'[^a-zA-Z0-9]+', '-', name).lower()
    sanitized = sanitized.strip('-')
    return sanitized

def get_local_logo_path(school):
    logo_url = school['Logo']
    if 'drive.google.com' not in logo_url:
        return logo_url
    sanitized = sanitize_filename(school['Name'])
    return f"img/{sanitized}.jpg"

def generate_school_cards(schools):
    cards = []
    for school in schools:
        card = f'''
        <div class="col-12 col-md-4">
          <div class="card h-100">
            <img src="{get_local_logo_path(school)}" class="card-img-top school-logo" alt="{school['Name']} Logo">
            <div class="card-body">
              <h5 class="card-title">
                <a href="{school['Website']}" class="text-decoration-none">{school['Name']}</a>
              </h5>
              <p class="card-text">{school['Description']}</p>
              <p class="card-text"><small class="text-muted">{school['Address']}</small></p>
              <a href="{school['Website']}" class="btn btn-primary">Visit Website</a>
            </div>
          </div>
        </div>'''
        cards.append(card)
    return '\n'.join(cards)

def build_site():
    try:
        # Fetch CSV data from URL
        url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS5DPiVrMEHIFMWWZLUcmy4plA_RQ0gIJmG98PHUJ1LEdzobsfYoaf1io5GC2wP64im0qGG6AS8IBJl/pub?gid=1797278409&single=true&output=csv'
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Parse CSV data
        csv_reader = csv.DictReader(response.text.splitlines())
        schools = list(csv_reader)

        if not schools:
            print("No school data found!")
            return
            
        # Prepare schools data for map
        schools_data = {
            "type": "FeatureCollection",
            "features": []
        }

        for school in schools:
            if school.get('Coord'):
                try:
                    # Parse coordinates - assuming "lat, lon" format in Coord field
                    print(school['Coord'], school['Name']) 
                    lat_str, lon_str = school['Coord'].split(',')
                    coords = [float(lon_str.strip()), float(lat_str.strip())]  # GeoJSON uses [lon, lat]
                    
                    schools_data['features'].append({
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": coords
                        },
                        "properties": {
                            "name": school['Name'],
                            "website": school['Website'],
                            "address": school['Address']
                        }
                    })
                except (ValueError, KeyError):
                    print(f"Skipping invalid coordinates for {school.get('Name', 'unnamed school')}")

        # Load template
        with open('template.html') as f:
            template = f.read()

        # Generate school cards
        schools_html = generate_school_cards(schools)

        # Insert into template
        output = template.replace('<!--SCHOOLS_GO_HERE-->', schools_html)
        
        # Replace map data placeholders
        output = output.replace('//SCHOOLS_DATA_PLACEHOLDER', f'const schoolsData = {json.dumps(schools_data)};')

        # Write output
        with open('index.html', 'w') as f:
            f.write(output)

        print("Site built successfully from Google Sheets data!")
    except Exception as e:
        print(f"Error building site: {e}")

if __name__ == '__main__':
    build_site()
