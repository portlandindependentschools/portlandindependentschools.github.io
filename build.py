import csv
import requests
import os
import re
import json
from datetime import datetime

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
        <div class="col-12 col-md-4" itemscope itemtype="https://schema.org/EducationalOrganization">
          <div class="card h-100">
            <img src="{get_local_logo_path(school)}" 
                 class="card-img-top school-logo" 
                 alt="{school['Name']} Logo"
                 itemprop="image">
            <div class="card-body">
              <h5 class="card-title" itemprop="name">
                <a href="{school['Website']}" 
                   class="text-decoration-none" 
                   itemprop="url">{school['Name']}</a>
              </h5>
              <p class="card-text" itemprop="description">{school['Description']}</p>
              <p class="card-text" itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
                <small class="text-muted">
                  <span itemprop="streetAddress">{school['Address']}</span>
                </small>
              </p>
              <a href="{school['Website']}" class="btn btn-primary">Visit Website</a>
            </div>
          </div>
        </div>'''
        cards.append(card)
    return '\n'.join(cards)

def generate_sitemap(lastmod_date):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.portlandindependentschools.org/</loc>
    <lastmod>{lastmod_date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>'''

def build_site():
    try:
        # Fetch CSV data from URL
        url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS5DPiVrMEHIFMWWZLUcmy4plA_RQ0gIJmG98PHUJ1LEdzobsfYoaf1io5GC2wP64im0qGG6AS8IBJl/pub?gid=1797278409&single=true&output=csv'
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Parse CSV data
        csv_reader = csv.DictReader(response.text.splitlines())
        schools = list(csv_reader)

        # Get current date in sitemap format
        lastmod_date = datetime.now().strftime('%Y-%m-%d')
        
        # Generate and write sitemap
        with open('sitemap.xml', 'w') as f:
            f.write(generate_sitemap(lastmod_date))
            
        print("Generated sitemap.xml with lastmod:", lastmod_date)

        if not schools:
            print("No school data found!")
            return
            
        # Prepare schools data for map
        schools_data = {
            "type": "FeatureCollection",
            "features": []
        }

        for school in schools:
            try:
                # Parse coordinates - assuming "lat, lon" format in Coord field
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
                        "address": school['Address'],
                        "description": school['Description']
                    }
                })
            except (ValueError, KeyError):
                print(f"Skipping invalid coordinates for {school.get('Name', 'unnamed school')}: ", school.get('Coord'))

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
