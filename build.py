import json
import os

def generate_school_cards(schools):
    cards = []
    for school in schools:
        card = f'''
        <div class="col-12 col-md-4">
          <div class="card h-100">
            <img src="{school['logo']}" class="card-img-top school-logo" alt="{school['name']} Logo">
            <div class="card-body">
              <h5 class="card-title">
                <a href="{school['website']}" class="text-decoration-none">{school['name']}</a>
              </h5>
              <p class="card-text">{school['description']}</p>
              <a href="{school['website']}" class="btn btn-primary">Visit Website</a>
            </div>
          </div>
        </div>'''
        cards.append(card)
    return '\n'.join(cards)

def build_site():
    # Load school data
    with open('schools.json') as f:
        data = json.load(f)
    
    # Load template
    with open('template.html') as f:
        template = f.read()
    
    # Generate school cards
    schools_html = generate_school_cards(data['schools'])
    
    # Insert into template
    output = template.replace('<!--SCHOOLS_GO_HERE-->', schools_html)
    
    # Write output
    with open('index.html', 'w') as f:
        f.write(output)
    
    print("Site built successfully!")

if __name__ == '__main__':
    build_site()
