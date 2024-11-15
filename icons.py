import json

def load_icons():
    # Load the JSON data from the file
    with open('static/json/Brands.json', 'r') as file:
        brands_data = json.load(file)
    
    # Extract relevant icon data
    icons = []
    for icon in brands_data.get("icons", []):
        icon_name = icon.get("tags", [None])[0]  # Use the first tag as the name
        icon_path = icon.get("paths", [None])[0]  # SVG path data
        if icon_name and icon_path:
            icons.append({'name': icon_name, 'path': icon_path})
    return icons