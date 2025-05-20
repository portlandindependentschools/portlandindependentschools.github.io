import csv
import requests
import os

def generate_school_cards(schools):
    cards = []
    for school in schools:
        card = f'''
        <div class="col-12 col-md-4">
          <div class="card h-100">
            <img src="{school['Logo']}" class="card-img-top school-logo" alt="{school['Name']} Logo">
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
    # Fetch CSV data from URL
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS5DPiVrMEHIFMWWZLUcmy4plA_RQ0gIJmG98PHUJ1LEdzobsfYoaf1io5GC2wP64im0qGG6AS8IBJl/pub?gid=1797278409&single=true&output=csv'
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors
    
    # Parse CSV data
    csv_reader = csv.DictReader(response.text.splitlines())
    schools = list(csv_reader)
    
    # Load template
    with open('template.html') as f:
        template = f.read()
    
    # Generate school cards
    schools_html = generate_school_cards(schools)
    
    # Insert into template
    output = template.replace('<!--SCHOOLS_GO_HERE-->', schools_html)
    
    # Write output
    with open('index.html', 'w') as f:
        f.write(output)
    
    print("Site built successfully from Google Sheets data!")

if __name__ == '__main__':
    build_site()
