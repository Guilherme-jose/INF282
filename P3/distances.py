import requests
from math import radians, sin, cos, sqrt, atan2
import time
import csv

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

def get_distance(city1, city2):
    """
    Get distance between two cities using the Nominatim API.
    Returns distance in kilometers.
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params1 = {"q": f"{city1}, Rondônia, Brazil", "format": "json"}
        params2 = {"q": f"{city2}, Rondônia, Brazil", "format": "json"}
        headers = {"User-Agent": "DistanceCalculator/1.0"}
        
        response1 = requests.get(url, params=params1, headers=headers)
        response2 = requests.get(url, params=params2, headers=headers)
        response1.raise_for_status()
        response2.raise_for_status()
        
        data1 = response1.json()
        data2 = response2.json()
        
        if not data1 or not data2:
            return None
        
        lat1, lon1 = float(data1[0]['lat']), float(data1[0]['lon'])
        lat2, lon2 = float(data2[0]['lat']), float(data2[0]['lon'])
        
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

populations = {city: get_city_population(city) for city in cities}
print("\nCity Populations:")
for city, pop in sorted(populations.items(), key=lambda x: x[1], reverse=True):
    print(f"  - {city}: {pop:,}")

# Calculate distances between all cities and write to file as a matrix

n = len(cities)
distances_matrix = [[0.0] * n for _ in range(n)]

print("\nCalculating distances between cities...")
for i, city1 in enumerate(cities):
    for j, city2 in enumerate(cities):
        if i < j:
            distance = get_distance(city1, city2)
            if distance:
                distances_matrix[i][j] = distance
                distances_matrix[j][i] = distance
            time.sleep(10)  # Wait 10 seconds between requests to respect API rate limits

# Write matrix to CSV file
with open('distances_matrix.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([''] + cities)  # Header row with city names
    for i, city in enumerate(cities):
        writer.writerow([city] + distances_matrix[i])

print("Distance matrix saved to distances_matrix.csv")