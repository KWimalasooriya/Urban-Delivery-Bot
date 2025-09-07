import webbrowser

# Function to create and open Google Maps route
def open_google_maps_route(start_coords, end_coords):
    base_url = "https://www.google.com/maps/dir/?api=1"
    origin = f"{start_coords[0]},{start_coords[1]}"
    destination = f"{end_coords[0]},{end_coords[1]}"
    url = f"{base_url}&origin={origin}&destination={destination}&travelmode=walking"
    webbrowser.open(url)
    print(f"Opened Google Maps with walking route from {origin} to {destination}")

# Hardcoded latitude and longitude for the locations
start_coords = (6.9024, 79.8607)  # Department of Physics, University of Colombo
end_coords = (6.9000, 79.8590)    # College House, University of Colombo

# Open the route in Google Maps
open_google_maps_route(start_coords, end_coords)
