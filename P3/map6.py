import geobr
import geopandas as gpd
import folium
import pandas as pd
import math

print("Buscando dados oficiais do IBGE...")
# 1. Carrega o mapa de todos os municípios de Rondônia
muni_ro = geobr.read_municipality(code_muni="RO", year=2020)

# Mapeamento explícito de Tags para garantir a correspondência correta
lista_ordenada_cidades = [
    "Vilhena", "Ariquemes", "Cacoal", "Guajará-Mirim", "Ouro Preto do Oeste", 
    "Buritis", "Nova Mamoré", "Alta Floresta D'Oeste", "São Miguel do Guaporé", "Presidente Médici", 
    "Alvorada D'Oeste", "Costa Marques", "Alto Alegre dos Parecis", "Itapuã do Oeste", "Governador Jorge Teixeira", 
    "Vale do Anari", "Novo Horizonte do Oeste", "Corumbiara", "Vale do Paraíso", "Teixeirópolis", 
    "Parecis", "Rio Crespo", "Castanheiras", "Primavera de Rondônia", "Pimenteiras do Oeste"
]
tags_lista = ['VLN', 'AQM', 'CAC', 'GJM', 'OPO', 'BUR', 'NMM', 'AFO', 'SMG', 'PME', 'ADO', 'CMQ', 'AAP', 'ITO', 'GJT', 'VAN', 'NHO', 'CRB', 'VDP', 'TXP', 'PRC', 'RCR', 'CTN', 'PVR', 'PMO']
dict_tags = {c.lower().strip(): t for c, t in zip(lista_ordenada_cidades, tags_lista)}

# 2. Define os dados de transporte (Camada 1: Cidades -> PSAs)
dados_transporte = [
    {"origem": "Vilhena", "destino": "Vilhena", "qtde": 21930.2},
    {"origem": "Ariquemes", "destino": "Ariquemes", "qtde": 21834.0},
    {"origem": "Cacoal", "destino": "Cacoal", "qtde": 19656.0},
    {"origem": "Guajará-Mirim", "destino": "Guajará-Mirim", "qtde": 8718.8},
    {"origem": "Ouro Preto do Oeste", "destino": "Ouro Preto do Oeste", "qtde": 7736.8},
    {"origem": "Buritis", "destino": "Buritis", "qtde": 6129.8},
    {"origem": "Nova Mamoré", "destino": "Guajará-Mirim", "qtde": 5740.2},
    {"origem": "Alta Floresta D'Oeste", "destino": "Novo Horizonte do Oeste", "qtde": 4557.4},
    {"origem": "São Miguel do Guaporé", "destino": "Novo Horizonte do Oeste", "qtde": 4461.0},
    {"origem": "Presidente Médici", "destino": "Ouro Preto do Oeste", "qtde": 4088.6},
    {"origem": "Alvorada D'Oeste", "destino": "Novo Horizonte do Oeste", "qtde": 2744.0},
    {"origem": "Costa Marques", "destino": "Costa Marques", "qtde": 2702.0},
    {"origem": "Alto Alegre dos Parecis", "destino": "Novo Horizonte do Oeste", "qtde": 2447.4},
    {"origem": "Itapuã do Oeste", "destino": "Ouro Preto do Oeste", "qtde": 1845.6},
    {"origem": "Governador Jorge Teixeira", "destino": "Ouro Preto do Oeste", "qtde": 1668.0},
    {"origem": "Vale do Anari", "destino": "Ouro Preto do Oeste", "qtde": 1644.0},
    {"origem": "Novo Horizonte do Oeste", "destino": "Novo Horizonte do Oeste", "qtde": 1594.4},
    {"origem": "Corumbiara", "destino": "Cacoal", "qtde": 1593.6},
    {"origem": "Vale do Paraíso", "destino": "Ouro Preto do Oeste", "qtde": 1358.0},
    {"origem": "Teixeirópolis", "destino": "Ouro Preto do Oeste", "qtde": 904.2},
    {"origem": "Parecis", "destino": "Novo Horizonte do Oeste", "qtde": 874.4},
    {"origem": "Rio Crespo", "destino": "Ouro Preto do Oeste", "qtde": 753.4},
    {"origem": "Castanheiras", "destino": "Novo Horizonte do Oeste", "qtde": 690.0},
    {"origem": "Primavera de Rondônia", "destino": "Novo Horizonte do Oeste", "qtde": 653.6},
    {"origem": "Pimenteiras do Oeste", "destino": "Cacoal", "qtde": 461.8}
]
df_transporte = pd.DataFrame(dados_transporte)

# Novos dados (Camada 2: PSAs -> Hospitais)
dados_hospital = [
    {"origem": "Vilhena", "destino": "Presidente Médici", "qtde": 2193.0},
    {"origem": "Ariquemes", "destino": "Presidente Médici", "qtde": 2183.4},
    {"origem": "Cacoal", "destino": "Presidente Médici", "qtde": 2171.1},
    {"origem": "Guajará-Mirim", "destino": "Presidente Médici", "qtde": 1445.9},
    {"origem": "Ouro Preto do Oeste", "destino": "Presidente Médici", "qtde": 1999.9},
    {"origem": "Buritis", "destino": "Presidente Médici", "qtde": 613.0},
    {"origem": "Costa Marques", "destino": "Presidente Médici", "qtde": 270.2},
    {"origem": "Novo Horizonte do Oeste", "destino": "Presidente Médici", "qtde": 1802.2}
]
df_hospital = pd.DataFrame(dados_hospital)

# Listas de nós para categorização logística (ATUALIZADA PARA 8 PSAs)
psas = ["Vilhena", "Ariquemes", "Cacoal", "Guajará-Mirim", "Ouro Preto do Oeste", "Buritis", "Costa Marques", "Novo Horizonte do Oeste"]
hospitais = ["Presidente Médici"]

psas_norm = [c.lower().strip() for c in psas]
hospitais_norm = [c.lower().strip() for c in hospitais]

# Une todas as cidades envolvidas no estudo
cidades_alvo = list(set(df_transporte['origem'].unique().tolist() + df_transporte['destino'].unique().tolist() + df_hospital['destino'].unique().tolist()))
cidades_alvo_norm = [c.lower().strip() for c in cidades_alvo]

# Normaliza nomes no GeoDataFrame do IBGE
muni_ro['name_muni_norm'] = muni_ro['name_muni'].str.lower().str.strip()
muni_filtrados = muni_ro[muni_ro['name_muni_norm'].isin(cidades_alvo_norm)]

# 3. Calcula os centroides de cada município
coords_cidades = {}
for _, row in muni_filtrados.iterrows():
    centroid = row['geometry'].representative_point()
    coords_cidades[row['name_muni_norm']] = [centroid.y, centroid.x]

# 4. Cria o mapa interativo
mapa = folium.Map(location=[-10.8, -63.0], zoom_start=7, 
                    tiles="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png",
                    attr="&copy; OpenStreetMap contributors &copy; CARTO")

# Fundo neutro para o estado
folium.GeoJson(
    muni_ro,
    style_function=lambda style: {
        'fillColor': '#f4f4f4',
        'color': '#dcdcdc',
        'weight': 1,
        'fillOpacity': 0.4
    }
).add_to(mapa)

# 5. Desenha as rotas de fluxo
# Rota Tipo A: Cidades ➔ PSAs (Linha Contínua Escura)
for _, row in df_transporte.iterrows():
    origem_norm = row['origem'].lower().strip()
    destino_norm = row['destino'].lower().strip()
    qtde = row['qtde']
    
    if origem_norm != destino_norm:
        if origem_norm in coords_cidades and destino_norm in coords_cidades:
            coord_orig = coords_cidades[origem_norm]
            coord_dest = coords_cidades[destino_norm]
            
            mid_lat = (coord_orig[0] + coord_dest[0]) / 2
            mid_lon = (coord_orig[1] + coord_dest[1]) / 2
            control_point = [mid_lat + 0.15, mid_lon + 0.15]
            
            points = []
            for t in [i/100.0 for i in range(101)]:
                lat = (1-t)**2 * coord_orig[0] + 2*(1-t)*t * control_point[0] + t**2 * coord_dest[0]
                lon = (1-t)**2 * coord_orig[1] + 2*(1-t)*t * control_point[1] + t**2 * coord_dest[1]
                points.append([lat, lon])
            
            folium.PolyLine(
                locations=points,
                color="#2c3e50",
                weight=1 + 4 * (qtde / 10000),
                opacity=0.7,
                tooltip=f"<b>Fluxo Primário:</b> {row['origem']} ➔ {row['destino']}<br><b>Pacientes/Ano:</b> {qtde:,.1f}"
            ).add_to(mapa)

# Rota Tipo B: PSAs ➔ Hospitais (Linha Tracejada Roxa)
for _, row in df_hospital.iterrows():
    origem_norm = row['origem'].lower().strip()
    destino_norm = row['destino'].lower().strip()
    qtde = row['qtde']
    
    if origem_norm != destino_norm:
        if origem_norm in coords_cidades and destino_norm in coords_cidades:
            coord_orig = coords_cidades[origem_norm]
            coord_dest = coords_cidades[destino_norm]
            
            mid_lat = (coord_orig[0] + coord_dest[0]) / 2
            mid_lon = (coord_orig[1] + coord_dest[1]) / 2
            control_point = [mid_lat - 0.15, mid_lon - 0.15]
            
            points = []
            for t in [i/100.0 for i in range(101)]:
                lat = (1-t)**2 * coord_orig[0] + 2*(1-t)*t * control_point[0] + t**2 * coord_dest[0]
                lon = (1-t)**2 * coord_orig[1] + 2*(1-t)*t * control_point[1] + t**2 * coord_dest[1]
                points.append([lat, lon])
            
            folium.PolyLine(
                locations=points,
                color="#9c27b0",
                weight=1.5 + 3 * (qtde / 2500),
                dash_array='5, 5',
                opacity=0.9,
                tooltip=f"<b>Transferência (Hospital):</b> {row['origem']} ➔ {row['destino']}<br><b>Pacientes/Ano:</b> {qtde:,.1f}"
            ).add_to(mapa)

# 6. Destaca municípios e adiciona os Marcadores Logísticos
for _, row in muni_filtrados.iterrows():
    nome = row['name_muni']
    nome_norm = row['name_muni_norm']
    centroid = row['geometry'].representative_point()
    
    is_hospital = nome_norm in hospitais_norm
    is_psa = nome_norm in psas_norm
    
    # Define as cores e tamanhos por nível de hierarquia
    if is_hospital:
        fill_color, border_color = '#9c27b0', '#4a148c'
        radius = 12
    elif is_psa:
        fill_color, border_color = '#e74c3c', '#b71c1c'
        radius = 9
    else:
        fill_color, border_color = '#3498db', '#1a5276'
        radius = 6

    # Texto personalizado para os Balões (Popups)
    if is_hospital:
        total_hosp = df_hospital[df_hospital['destino'].str.lower().str.strip() == nome_norm]['qtde'].sum()
        popup_text = f"<b>🏥 HOSPITAL ATIVO: {nome}</b><br>Total Recebido (Alta Complexidade): {total_hosp:,.1f} pac/ano"
        if nome_norm in df_transporte['origem'].str.lower().str.strip().values:
            dst = df_transporte[df_transporte['origem'].str.lower().str.strip() == nome_norm]['destino'].iloc[0]
            qt = df_transporte[df_transporte['origem'].str.lower().str.strip() == nome_norm]['qtde'].iloc[0]
            popup_text += f"<br><br><i>Triagem Local: Envia {qt:,.1f} para o PSA de {dst}</i>"
    elif is_psa:
        total_psa = df_transporte[df_transporte['destino'].str.lower().str.strip() == nome_norm]['qtde'].sum()
        total_env_hosp = df_hospital[df_hospital['origem'].str.lower().str.strip() == nome_norm]['qtde'].sum()
        popup_text = f"<b>🏪 PSA ATIVO: {nome}</b><br>Recebido das Cidades: {total_psa:,.1f} pac/ano<br>Enviado p/ Hospital (10%): {total_env_hosp:,.1f} pac/ano"
    else:
        destino = df_transporte[df_transporte['origem'].str.lower().str.strip() == nome_norm]['destino'].iloc[0]
        qtde = df_transporte[df_transporte['origem'].str.lower().str.strip() == nome_norm]['qtde'].iloc[0]
        popup_text = f"<b>📍 Cidade Origem: {nome}</b><br>Encaminha para PSA: {destino}<br>Pacientes/Ano: {qtde:,.1f}"

    # Estiliza o polígono do município no mapa de fundo
    folium.GeoJson(
        row['geometry'],
        style_function=lambda style, fc=fill_color, bc=border_color: {
            'fillColor': fc,
            'color': bc,
            'weight': 1.5,
            'fillOpacity': 0.25 if radius == 6 else 0.45
        }
    ).add_to(mapa)
    
    # Adiciona o círculo indicador do ponto físico
    folium.CircleMarker(
        location=[centroid.y, centroid.x],
        radius=radius,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=f"{nome} ({'Hospital' if is_hospital else ('PSA' if is_psa else 'Origem')})",
        color=border_color,
        fill=True,
        fillColor=fill_color,
        fillOpacity=0.9,
        weight=2
    ).add_to(mapa)
    
    # Adiciona a caixa de texto flutuante com a sigla (Tag)
    tag_nome = dict_tags.get(nome_norm, "???")
    folium.Marker(
        location=[centroid.y, centroid.x],
        icon=folium.DivIcon(html=f'''
            <div style="font-size: 9px; font-weight: bold; color: black; 
                        text-align: center; background-color: rgba(255,255,255,0.75); 
                        border: 1px solid {border_color}; border-radius: 5px; 
                        padding: 1px 3px; margin-left: 12px; margin-top: -8px; 
                        white-space: nowrap; display: inline-block;">
                {tag_nome}
            </div>
        ''')
    ).add_to(mapa)

# 7. Desenha o contorno geográfico forte do estado de Rondônia
estado_ro = geobr.read_state(code_state="RO", year=2020)
folium.GeoJson(
    estado_ro,
    style_function=lambda style: {
        'fillColor': 'none',
        'color': '#333333',
        'weight': 2.5,
        'fillOpacity': 0
    }
).add_to(mapa)

# Salva o resultado final
mapa.save("mapa_rondonia_8_psas_1_hospital.html")
print("Sucesso! O mapa foi salvo como 'mapa_rondonia_8_psas_1_hospital.html'.")