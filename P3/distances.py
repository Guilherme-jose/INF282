import requests
from math import radians, sin, cos, sqrt, atan2
import time
import csv


GEOCODE_CACHE = {}

def get_cities_in_rondonia():
    """
    Fetch all cities in the state of Rondônia, Brazil using the IBGE API.
    Returns a list of city names.
    """
    try:
        # IBGE API endpoint for Rondônia (state code 23)
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/RO/municipios"
        response = requests.get(url)
        response.raise_for_status()
        
        cities = response.json()
        city_names = [city['nome'] for city in cities]
        
        return sorted(city_names)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cities: {e}")
        return []


cities = get_cities_in_rondonia()
print(f"Cities in Rondônia: {len(cities)}")
for city in cities:
    print(f"  - {city}")

def geocode_city(city):
    """
    Get latitude and longitude for a city using Nominatim.
    Results are cached to avoid repeated requests.
    """
    if city in GEOCODE_CACHE:
        return GEOCODE_CACHE[city]

    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": f"{city}, Rondônia, Brazil", "format": "json", "limit": 1}
    headers = {"User-Agent": "DistanceCalculator/1.0 (INF282 project)"}

    delay = 1
    for attempt in range(5):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            if response.status_code == 429:
                time.sleep(delay)
                delay *= 2
                continue

            response.raise_for_status()
            data = response.json()
            if not data:
                return None

            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            GEOCODE_CACHE[city] = (lat, lon)
            time.sleep(1)  # Respect Nominatim rate limits
            return GEOCODE_CACHE[city]
        except requests.exceptions.RequestException as e:
            if attempt == 4:
                print(f"Error geocoding {city}: {e}")
                return None
            time.sleep(delay)
            delay *= 2


def get_distance(city1, city2):
    """
    Get distance between two cities using cached Nominatim geocodes.
    Returns distance in kilometers.
    """
    try:
        coord1 = geocode_city(city1)
        coord2 = geocode_city(city2)

        if not coord1 or not coord2:
            return None

        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        # Haversine formula
        R = 6371  # Earth radius in km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c
    except Exception as e:
        print(f"Error getting distance between {city1} and {city2}: {e}")
        return None

def get_city_population(city):
    """
    Get population of a city using the IBGE API.
    Returns population as an integer.
    """
    try:
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        response = requests.get(url)
        response.raise_for_status()
        
        cities_data = response.json()
        for city_data in cities_data:
            if city_data['nome'].lower() == city.lower() and city_data['microrregiao']['mesorregiao']['UF']['sigla'] == 'RO':
                return city_data.get('populacao', 0)
        return 0
    except Exception as e:
        print(f"Error getting population for {city}: {e}")
        return 0


# Calculate distances between all cities and write to file as a matrix

n = len(cities)
distances_matrix = [[0.0] * n for _ in range(n)]

print("\nCalculating distances between cities...")
for i, city1 in enumerate(cities):
    for j, city2 in enumerate(cities):
        if i < j:
            distance = get_distance(city1, city2)
            if distance is not None:
                distances_matrix[i][j] = distance
                distances_matrix[j][i] = distance
            time.sleep(0.2)

# Write matrix to CSV file
with open('distances_matrix.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([''] + cities)  # Header row with city names
    for i, city in enumerate(cities):
        writer.writerow([city] + distances_matrix[i])

print("Distance matrix saved to distances_matrix.csv")