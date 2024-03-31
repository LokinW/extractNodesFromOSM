import json
import os
import osmium

class PlaygroundSchoolHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.playgrounds = []
        self.schools = []
        self.sport_locations = []
        self.kindergartens = []
        self.childcare = []

    def node(self, n):
        tags = dict(n.tags)
        leisure_tag = tags.get('leisure')
        amenity_tag = tags.get('amenity')
        building_tag = tags.get('building')
        sport_tag = tags.get('sport')
        name_tag = tags.get('name')

        id = getattr(n, 'id', None)
        latitude = getattr(n.location, 'lat', None)
        longitude = getattr(n.location, 'lon', None)

        location = {
            'id': id,
            'latitude': latitude,
            'longitude': longitude,
            'name': name_tag
        }

        if leisure_tag == 'playground':
            self.playgrounds.append(location)
        elif amenity_tag == 'school' or building_tag == 'school':
            self.schools.append(location)
        elif amenity_tag == 'kindergarten':
            self.kindergartens.append(location)
        elif amenity_tag == 'childcare':
            self.childcare.append(location)
        elif sport_tag:
            location['sport'] = sport_tag
            self.sport_locations.append(location)

# Replace 'your_input_file.pbf' with the path to your OSM PBF file
input_file = 'germany-latest.osm.pbf'
handler = PlaygroundSchoolHandler()

print("Loading and processing OSM data...")
try:
    handler.apply_file(input_file)
except Exception as e:
    print("An error occurred while processing the file:", str(e))
    exit()

# Convert extracted data to JSON
data = {
    'playgrounds': handler.playgrounds,
    'schools': handler.schools,
    'sport_locations': handler.sport_locations,
    'kindergartens': handler.kindergartens,
    'childcare': handler.childcare
}

# Write JSON data to file
output_file = 'germany-latest.json'
if os.path.exists(output_file):
    overwrite = input(f"The file '{output_file}' already exists. Do you want to overwrite it? (y/n): ")
    if overwrite.lower() != 'y':
        print("Operation canceled.")
        exit()

print(f"Writing JSON data to {output_file}...")
with open(output_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Extraction and conversion completed.")
print(f"Extracted {len(handler.playgrounds)} playgrounds, {len(handler.schools)} schools, {len(handler.sport_locations)} sport locations, {len(handler.kindergartens)} kindergartens, and {len(handler.childcare)} childcare facilities.")
print(f"JSON data written to {output_file}.")
