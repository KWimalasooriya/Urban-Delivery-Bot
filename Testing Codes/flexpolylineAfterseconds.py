import requests
import time
import webbrowser
import flexpolyline

# Function to get a route from HERE Maps API
def get_route(start_coords, end_coords):
    api_key = "D5XKY2CgODfY3CIUyzTCtmj1cTVZzgAtqoPTpqy1S-4"
    url = f"https://router.hereapi.com/v8/routes?apiKey={api_key}&origin={start_coords[0]},{start_coords[1]}&destination={end_coords[0]},{end_coords[1]}&transportMode=pedestrian"
    
    response = requests.get(url)
    if response.status_code == 200:
        route_data = response.json()
        if "routes" in route_data and len(route_data["routes"]) > 0:
            return route_data["routes"][0]["sections"]
    return None

# Function to simulate driving the robot along the route
def drive_robot(route_sections):
    for section in route_sections:
        if "polyline" in section:
            polyline = section["polyline"]
            coordinates = decode_polyline(polyline)
            
            for waypoint in coordinates:
                print(f"Driving to waypoint: {waypoint}")
                # Simulate sending waypoint to the robot's control system
                # robot.drive_to(waypoint[0], waypoint[1])
                time.sleep(1)  # Simulate driving time
        print("Section completed!")

# Decode polyline (HERE uses a flexible polyline encoding)
def decode_polyline(encoded_polyline):
    return flexpolyline.decode(encoded_polyline)

# Function to open Google Maps with a walking route
def open_google_maps_route(start_coords, end_coords):
    base_url = "https://www.google.com/maps/dir/?api=1"
    origin = f"{start_coords[0]},{start_coords[1]}"
    destination = f"{end_coords[0]},{end_coords[1]}"
    url = f"{base_url}&origin={origin}&destination={destination}&travelmode=walking"
    time.sleep(3)  # Wait for 3 seconds before opening the map
    webbrowser.open(url)
    print(f"Opened Google Maps with walking route from {origin} to {destination}")

# Hardcoded starting and ending coordinates
start_coords = (6.9024, 79.8607)  # Department of Physics
end_coords = (6.9017, 79.8628)    # College House

# Get the route from HERE Maps API
route_sections = get_route(start_coords, end_coords)

if route_sections:
    print("Route obtained. Driving the robot...")
    drive_robot(route_sections)
    # Show the walking route in Google Maps
    open_google_maps_route(start_coords, end_coords)
else:
    print("Failed to get a route.")
