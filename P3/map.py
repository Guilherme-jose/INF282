import geobr
import geopandas as gpd
import folium

print("Buscando dados oficiais do IBGE...")
# 1. Carrega o mapa de todos os municípios de Rondônia
muni_ro = geobr.read_municipality(code_muni="RO", year=2020)

# Sua lista de cidades
cidades_alvo = [
    "Vilhena", "Ariquemes", "Cacoal", "Guajará-Mirim", "Ouro Preto do Oeste", 
    "Buritis", "Nova Mamoré", "Alta Floresta D'Oeste", "São Miguel do Guaporé", 
    "Presidente Médici", "Alvorada D'Oeste", "Costa Marques", "Alto Alegre dos Parecis", 
    "Itapuã do Oeste", "Governador Jorge Teixeira", "Vale do Anari", "Novo Horizonte do Oeste", 
    "Corumbiara", "Vale do Paraíso", "Teixeirópolis", "Parecis", "Rio Crespo", 
    "Castanheiras", "Primavera de Rondônia", "Pimenteiras do Oeste"
]

# Normaliza os nomes para evitar erros de maiúsculas/minúsculas ou espaços
cidades_alvo_norm = [c.lower().strip() for c in cidades_alvo]
muni_ro['name_muni_norm'] = muni_ro['name_muni'].str.lower().str.strip()

# Filtra o mapa apenas com as cidades da sua lista
muni_filtrados = muni_ro[muni_ro['name_muni_norm'].isin(cidades_alvo_norm)]

# 2. Cria o mapa interativo centrado geograficamente em Rondônia
mapa = folium.Map(location=[-10.8, -63.0], zoom_start=7, 
                    tiles="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png",
                    attr="&copy; OpenStreetMap contributors &copy; CARTO")

# Adiciona o contorno cinza de fundo de todas as cidades de RO
folium.GeoJson(
    muni_ro,
    style_function=lambda style: {
        'fillColor': '#f4f4f4',
        'color': '#c0c0c0',
        'weight': 1,
        'fillOpacity': 0.4
    }
).add_to(mapa)

# Adiciona as cidades selecionadas destacadas em azul
for _, row in muni_filtrados.iterrows():
    # Destaca o polígono do município
    folium.GeoJson(
        row['geometry'],
        style_function=lambda style: {
            'fillColor': '#3182bd',
            'color': '#1c3d5a',
            'weight': 1.5,
            'fillOpacity': 0.6
        }
    ).add_to(mapa)
    
    # Usa a localização oficial do município
    centroid = row['geometry'].representative_point()
    
    # Cria label abreviado (3 primeiras letras)
    label = row['name_muni'].upper()
    
    # Adiciona círculo com label abreviado
    folium.CircleMarker(
        location=[centroid.y, centroid.x],
        radius=8,
        popup=f"<b>{row['name_muni']}</b>",
        tooltip=row['name_muni'],
        color='#1c3d5a',
        fill=True,
        fillColor='#3182bd',
        fillOpacity=0.8,
        weight=2
    ).add_to(mapa)
    
    # Adiciona o label de texto no mapa
    folium.Marker(
        location=[centroid.y, centroid.x],
        icon=folium.DivIcon(html=f'''
            <div style="font-size: 10px; font-weight: bold; color: black; 
                        text-align: center; background-color: rgba(0,0,0,0); 
                        border-radius: 3px; padding: 2px 4px; margin-left: 10px; white-space: nowrap;">
                {label}
            </div>
        ''')
    ).add_to(mapa)

# 3. Adiciona o outline (contorno) do estado de Rondônia
estado_ro = geobr.read_state(code_state="RO", year=2020)
folium.GeoJson(
    estado_ro,
    style_function=lambda style: {
        'fillColor': 'none',
        'color': '#000000',
        'weight': 3,
        'fillOpacity': 0
    }
).add_to(mapa)

# Salva o resultado em um arquivo HTML
mapa.save("mapa_rondonia_interativo.html")
print("Sucesso! O mapa foi salvo como 'mapa_rondonia_interativo.html'. Abra-o no seu navegador.")
