import pandas as pd
from pathlib import Path

RO = {
"Alta Floresta D'Oeste": 1100015,
"Alto Alegre dos Parecis": 1100379,
"Alto Paraíso": 1100403,
"Alvorada D'Oeste": 1100346,
"Ariquemes": 1100023,
"Buritis": 1100452,
"Cabixi": 1100031,
"Cacaulândia": 1100601,
"Cacoal": 1100049,
"Campo Novo de Rondônia": 1100700,
"Candeias do Jamari": 1100809,
"Castanheiras": 1100908,
"Cerejeiras": 1100056,
"Chupinguaia": 1100924,
"Colorado do Oeste": 1100064,
"Corumbiara": 1100072,
"Costa Marques": 1100080,
"Cujubim": 1100940,
"Espigão d'Oeste": 1100098,
"Governador Jorge Teixeira": 1101005,
"Guajará-Mirim": 1100106,
"Itapuã do Oeste": 1101104,
"Jaru": 1100114,
"Ji-Paraná": 1100122,
"Machadinho d'Oeste": 1100130,
"Ministro Andreazza": 1101203,
"Mirante da Serra": 1101302,
"Monte Negro": 1101401,
"Nova Brasilândia d'Oeste": 1100148,
"Nova Mamoré": 1100338,
"Nova União": 1101435,
"Novo Horizonte do Oeste": 1100502,
"Ouro Preto do Oeste": 1100155,
"Parecis": 1101450,
"Pimenta Bueno": 1100189,
"Pimenteiras do Oeste": 1101468,
"Porto Velho": 1100205,
"Presidente Médici": 1100254,
"Primavera de Rondônia": 1101476,
"Rio Crespo": 1100262,
"Rolim de Moura": 1100288,
"Santa Luzia d'Oeste": 1100296,
"São Felipe d'Oeste": 1101484,
"São Francisco do Guaporé": 1101492,
"São Miguel do Guaporé": 1100320,
"Seringueiras": 1101500,
"Teixeirópolis": 1101559,
"Theobroma": 1101609,
"Urupá": 1101708,
"Vale do Anari": 1101757,
"Vale do Paraíso": 1101807,
"Vilhena": 1100304
}

cities = ["Vilhena", "Ariquemes", "Cacoal", "Guajará-Mirim", "Ouro Preto do Oeste", 
        "Buritis", "Nova Mamoré", "Alta Floresta D'Oeste", "São Miguel do Guaporé", 
        "Presidente Médici", "Alvorada D'Oeste", "Costa Marques", "Alto Alegre dos Parecis", 
        "Itapuã do Oeste", "Governador Jorge Teixeira", "Vale do Anari", "Novo Horizonte do Oeste", 
        "Corumbiara", "Vale do Paraíso", "Teixeirópolis", "Parecis", "Rio Crespo", 
        "Castanheiras", "Primavera de Rondônia", "Pimenteiras do Oeste"]

# Filter RO to keep only cities in sCid, in the order they appear in sCid
RO = {city: RO[city] for city in cities if city in RO}
if len(RO) != len(cities):
    missing = set(cities) - set(RO.keys())
    print(f"Warning: The following cities were not found in RO and will be skipped: {missing}")

base_dir = Path(__file__).resolve().parent
input_csv = base_dir / "dist_brasil.csv"
output_csv = base_dir / "dist_rondonia.csv"

if not input_csv.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {input_csv}")

df = pd.read_csv(input_csv, sep=';')

ro_codes = set(RO.values())
df = df[(df['orig'].isin(ro_codes)) & (df['dest'].isin(ro_codes))]

# Convert distances from meters to kilometers
df['dist'] = df['dist'] / 1000

# Make matrix symmetric and set diagonal to 5
for idx, row in df.iterrows():
    orig, dest, dist = row['orig'], row['dest'], row['dist']
    # Add reverse direction if not exists
    reverse = df[(df['orig'] == dest) & (df['dest'] == orig)]
    if reverse.empty:
        df = pd.concat([df, pd.DataFrame({'orig': [dest], 'dest': [orig], 'dist': [dist]})], ignore_index=True)

# Set distance from each city to itself to 5
for city_code in ro_codes:
    df.loc[(df['orig'] == city_code) & (df['dest'] == city_code), 'dist'] = 5


# Create reverse mapping from codes to names
code_to_name = {v: k for k, v in RO.items()}

# Replace codes with names
df['orig'] = df['orig'].map(code_to_name)
df['dest'] = df['dest'].map(code_to_name)


# Write to new CSV
df.to_csv(output_csv, index=False)

# Write to .txt
with open(base_dir / "dist_rondonia.txt", 'w') as f:
    for city in cities:
        f.write(f"{city}, ")

    f.write("Distâncias entre as cidades\n")
    f.write("Dist:: [ ")
    
    distances = []
    for orig in cities:
        for dest in cities:
            dist = df[(df['orig'] == orig) & (df['dest'] == dest)]['dist'].values
            dist_val = int(dist[0]) if len(dist) > 0 else 5
            distances.append(f"{dist_val:3d}")
    
    for i, distance in enumerate(distances):
        if i > 0 and i % len(cities) == 0:
            f.write("\n")
        f.write(distance)
        if i < len(distances) - 1:
            f.write(", ")
    
    f.write(" ]\n")