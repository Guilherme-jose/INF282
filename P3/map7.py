import geobr
import geopandas as gpd
import folium
import pandas as pd
import math

print("Buscando dados oficiais do IBGE...")
# 1. Carrega o mapa de todos os municípios de Rondônia
muni_ro = geobr.read_municipality(code_muni="RO", year=2020)

tags = [
    'VLN', 'AQM', 'CAC', 'GJM', 'OPO', 
    'BUR', 'NMM', 'AFO', 'SMG', 'PME', 
    'ADO', 'CMQ', 'AAP', 'ITO', 'GJT', 
    'VAN', 'NHO', 'CRB', 'VDP', 'TXP', 
    'PRC', 'RCR', 'CTN', 'PVR', 'PMO'
]

# 2. Define os novos dados de transporte fornecidos (Todos para Presidente Médici)
dados_transporte = [
    {"origem": "Vilhena", "destino": "Presidente Médici", "qtde": 21930},
    {"origem": "Ariquemes", "destino": "Presidente Médici", "qtde": 21834},
    {"origem": "Cacoal", "destino": "Presidente Médici", "qtde": 19656},
    {"origem": "Guajará-Mirim", "destino": "Presidente Médici", "qtde": 8719},
    {"origem": "Ouro Preto do Oeste", "destino": "Presidente Médici", "qtde": 7737},
    {"origem": "Buritis", "destino": "Presidente Médici", "qtde": 6130},
    {"origem": "Nova Mamoré", "destino": "Presidente Médici", "qtde": 5740},
    {"origem": "Alta Floresta D'Oeste", "destino": "Presidente Médici", "qtde": 4557},
    {"origem": "São Miguel do Guaporé", "destino": "Presidente Médici", "qtde": 4461},
    {"origem": "Presidente Médici", "destino": "Presidente Médici", "qtde": 4089},
    {"origem": "Alvorada D'Oeste", "destino": "Presidente Médici", "qtde": 2744},
    {"origem": "Costa Marques", "destino": "Presidente Médici", "qtde": 2702},
    {"origem": "Alto Alegre dos Parecis", "destino": "Presidente Médici", "qtde": 2447},
    {"origem": "Itapuã do Oeste", "destino": "Presidente Médici", "qtde": 1846},
    {"origem": "Governador Jorge Teixeira", "destino": "Presidente Médici", "qtde": 1668},
    {"origem": "Vale do Anari", "destino": "Presidente Médici", "qtde": 1644},
    {"origem": "Novo Horizonte do Oeste", "destino": "Presidente Médici", "qtde": 1594},
    {"origem": "Corumbiara", "destino": "Presidente Médici", "qtde": 1594},
    {"origem": "Vale do Paraíso", "destino": "Presidente Médici", "qtde": 1358},
    {"origem": "Teixeirópolis", "destino": "Presidente Médici", "qtde": 904},
    {"origem": "Parecis", "destino": "Presidente Médici", "qtde": 874},
    {"origem": "Rio Crespo", "destino": "Presidente Médici", "qtde": 753},
    {"origem": "Castanheiras", "destino": "Presidente Médici", "qtde": 690},
    {"origem": "Primavera de Rondônia", "destino": "Presidente Médici", "qtde": 654},
    {"origem": "Pimenteiras do Oeste", "destino": "Presidente Médici", "qtde": 462}
]
df_transporte = pd.DataFrame(dados_transporte)

# Lista de PSAs atualizada (Apenas Presidente Médici)
psas = ["Presidente Médici"]
psas_norm = [c.lower().strip() for c in psas]

# Cidades alvo (todas as origens)
cidades_alvo = df_transporte['origem'].unique().tolist()
cidades_alvo_norm = [c.lower().strip() for c in cidades_alvo]

# Normaliza nomes no GeoDataFrame
muni_ro['name_muni_norm'] = muni_ro['name_muni'].str.lower().str.strip()
muni_filtrados = muni_ro[muni_ro['name_muni_norm'].isin(cidades_alvo_norm)]

# 3. Calcula e armazena as coordenadas (centroides) de cada cidade para traçar as linhas
coords_cidades = {}
for _, row in muni_filtrados.iterrows():
    centroid = row['geometry'].representative_point()
    coords_cidades[row['name_muni_norm']] = [centroid.y, centroid.x]

# 4. Cria o mapa interativo
mapa = folium.Map(location=[-10.8, -63.0], zoom_start=7, 
                    tiles="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png",
                    attr="&copy; OpenStreetMap contributors &copy; CARTO")

# Fundo cinza para o estado
folium.GeoJson(
    muni_ro,
    style_function=lambda style: {
        'fillColor': '#f4f4f4',
        'color': '#c0c0c0',
        'weight': 1,
        'fillOpacity': 0.4
    }
).add_to(mapa)

# 5. Adiciona os fluxos (Linhas de transporte das Origens para os PSAs)
for _, row in df_transporte.iterrows():
    origem_norm = row['origem'].lower().strip()
    destino_norm = row['destino'].lower().strip()
    qtde = row['qtde']
    
    # Se a cidade não envia para si mesma, desenha uma linha
    if origem_norm != destino_norm:
        if origem_norm in coords_cidades and destino_norm in coords_cidades:
            coord_orig = coords_cidades[origem_norm]
            coord_dest = coords_cidades[destino_norm]
            
            # Calculate control point for Bezier curve
            mid_lat = (coord_orig[0] + coord_dest[0]) / 2
            mid_lon = (coord_orig[1] + coord_dest[1]) / 2
            offset = 0.2
            control_point = [mid_lat + offset, mid_lon + offset]
            
            # Generate Bezier curve points (100 intermediate points)
            points = []
            for t in [i/100.0 for i in range(101)]:
                lat = (1-t)**2 * coord_orig[0] + 2*(1-t)*t * control_point[0] + t**2 * coord_dest[0]
                lon = (1-t)**2 * coord_orig[1] + 2*(1-t)*t * control_point[1] + t**2 * coord_dest[1]
                points.append([lat, lon])
            
            folium.PolyLine(
                locations=points,
                color="#000000",
                weight=1 + 5 * (qtde / 5000),
                opacity=1,
                tooltip=f"<b>Rota:</b> {row['origem']} ➔ {row['destino']}<br><b>Qtde:</b> {qtde}"
            ).add_to(mapa)

# 6. Destaca as cidades e adiciona os marcadores
for _, row in muni_filtrados.iterrows():
    nome = row['name_muni']
    nome_norm = row['name_muni_norm']
    centroid = row['geometry'].representative_point()
    
    # Define as cores dependendo se é PSA ou Origem
    is_psa = nome_norm in psas_norm
    fill_color = '#d62728' if is_psa else '#3182bd'  # Vermelho para PSA, Azul para Origem
    border_color = "#8c151572" if is_psa else "#1c3d5a6c"
    
    # Filtra dados para o Popup
    if is_psa:
        total = df_transporte[df_transporte['destino'].str.lower().str.strip() == nome_norm]['qtde'].sum()
        popup_text = f"<b>PSA: {nome}</b><br>Total Recebido: {total}"
    else:
        destino = df_transporte[df_transporte['origem'].str.lower().str.strip() == nome_norm]['destino'].iloc[0]
        qtde = df_transporte[df_transporte['origem'].str.lower().str.strip() == nome_norm]['qtde'].iloc[0]
        popup_text = f"<b>Origem: {nome}</b><br>Envia para: {destino}<br>Qtde: {qtde}"

    # Polígono do município
    folium.GeoJson(
        row['geometry'],
        style_function=lambda style, fc=fill_color, bc=border_color: {
            'fillColor': fc,
            'color': bc,
            'weight': 1.5,
            'fillOpacity': 0.5
        }
    ).add_to(mapa)
    
    # Círculo
    folium.CircleMarker(
        location=[centroid.y, centroid.x],
        radius=12 if is_psa else 6, # PSA fica com destaque maior por centralizar tudo
        popup=folium.Popup(popup_text, max_width=250),
        tooltip=f"{nome} ({'PSA' if is_psa else 'Origem'})",
        color=border_color,
        fill=True,
        fillColor=fill_color,
        fillOpacity=0.9,
        weight=2
    ).add_to(mapa)
    
    # Label de texto no mapa
    folium.Marker(
        location=[centroid.y, centroid.x],
        icon=folium.DivIcon(html=f'''
            <div style="font-size: 10px; font-weight: bold; color: black; 
                        text-align: center; background-color: rgba(255,255,255,0.6); 
                        border-radius: 10px; padding: 2px 5px; margin-left: 15px; margin-top: -10px; white-space: nowrap; display: inline-block;">
                {tags[cidades_alvo_norm.index(nome_norm)]}
            </div>
        ''')
    ).add_to(mapa)

# 7. Adiciona o contorno do estado de Rondônia
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

# Salva o resultado
mapa.save("mapa_rondonia_psas_logistica_2.html")
print("Sucesso! O mapa foi salvo como 'mapa_rondonia_psas_logistica.html'. Abra-o no seu navegador.")