'''
Author: Eddie Lowney
Description: Extracts FIPS codes using the Google Maps API
Date:
Output:
'''

import pandas as pd
import requests
import csv

import geopandas as gpd
from shapely.geometry import Point

data = pd.read_excel("Grant Data.xlsx")

# Google Maps API Key
API_KEY = "AIzaSyAh-6QncUJq02SG-0w7-K8HRkiQaewQUlQ"  # Replace with your actual Google API key

coordinate_list = []
COORDINATE_VAL = 0
# Function to get county from company name and state using Google Maps Geocoding API
def get_county_from_name_and_state(company_name, state):
    global COORDINATE_VAL
    print(COORDINATE_VAL)
    COORDINATE_VAL += 1
    # Geocode request URL
    address = f"{company_name}, {state}"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"

    # Send GET request to the Google Maps API
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the response
        data = response.json()
        if data["status"] == "OK":
            # Attempt to extract the county name
            try:
                # Checking if the address component contains the county
                location = data['results'][0]['geometry']['location']
                lat = location['lat']
                lng = location['lng']
                return lat, lng

            except (IndexError, KeyError):
                # If there is no county information, skip this entry
                print(
                    f"No county found for {company_name} in {state}. Skipping.")
                return None

state = list(data["State"])
recipient = list(data["Recipient"])
for i in range(len(state)):
    coordinate_list.append(get_county_from_name_and_state(recipient[i], state[i]))

file_path = "Coordinates.csv"
with open(file_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    for item in coordinate_list:
        writer.writerow([item])

# coordinate_list = [(36.778261, -119.4179324), (36.7739067, -119.8901977), None,
#                    (36.778261, -119.4179324), (35.2206515, -118.8239317),
#                    (38.3842914, -121.390908), (38.0215061, -120.398985),
#                    (36.988342, -121.5494688), (36.778261, -119.4179324),
#                    (36.5900189, -119.4490225)]

def get_fips_from_coordinates(lat, lon, shapefile_path):
    # Load the county shapefile into a GeoDataFrame
    counties = gpd.read_file(shapefile_path)
    # Create a Point geometry from the latitude and longitude
    point = Point(lon, lat)

    # Create a GeoDataFrame for the point
    point_gdf = gpd.GeoDataFrame(geometry=[point], crs=counties.crs)

    # Perform a spatial join between the point and the counties
    joined = gpd.sjoin(point_gdf, counties, how="left", predicate="within")

    # Extract the FIPS code (usually found in the 'GEOID' column)
    if not joined.empty:
        fips_code = joined.iloc[0]['GEOID']
        return fips_code
    else:
        print("Point is not within any county.")
        return None

# Example usage
value = 0
lat = 40.8665166
lon = -124.0828396
shapefile_path = 'tl_2024_us_county.shx'  # Replace with the path to your shapefile
fips_codes = []
for i in range(len(coordinate_list)):
    if coordinate_list[i] != None:
        print(value)
        fips_codes.append(get_fips_from_coordinates(
                    coordinate_list[i][0], coordinate_list[i][1], shapefile_path))
    else:
        fips_codes.append(None)
    value += 1
file_path = "FIPS_CODES.csv"
with open(file_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    for item in fips_codes:
        writer.writerow([item])
print(fips_codes)
