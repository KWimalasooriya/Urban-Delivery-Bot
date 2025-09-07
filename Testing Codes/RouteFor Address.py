import requests
import webbrowser

# Function to get coordinates from address
def geocode_address(address):
    api_key = "D5XKY2CgODfY3CIUyzTCtmj1cTVZzgAtqoPTpqy1S-4"
    url = f"https://geocode.search.hereapi.com/v1/geocode?q={address}&apiKey={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        geocode_data = response.json()
        if geocode_data["items"]:
            location = geocode_data["items"][0]["position"]
            return location["lat"], location["lng"]
    return None

# Example: From an address to route and open in Google Maps
address_start = "Colombo"
address_end = "Kandy"

# Get coordinates for both start and end addresses
start_coords = geocode_address(address_start)
end_coords = geocode_address(address_end)

if start_coords and end_coords:
    print(f"Start coordinates: {start_coords}")
    print(f"End coordinates: {end_coords}")

    # Create the Google Maps URL for routing
    google_maps_url = f"https://www.google.com/maps/dir/?api=1&origin={start_coords[0]},{start_coords[1]}&destination={end_coords[0]},{end_coords[1]}"
    
    # Open Google Maps in the default browser
    webbrowser.open(google_maps_url)
else:
    print("Failed to geocode addresses.")
