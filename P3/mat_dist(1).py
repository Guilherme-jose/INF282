from geopy.geocoders import Nominatim
import geopy.distance

def distancia(cid1, cid2):
    p1 = geolocator.geocode(f"{cid1}")
    p1 = (p1.latitude, p1.longitude)

    p2 = geolocator.geocode(f"{cid2}")
    p2 = (p2.latitude, p2.longitude)

    return int(geopy.distance.geodesic(p1, p2).km)

if __name__ == "__main__":
    geolocator = Nominatim(user_agent="Webscrapper")

    cidades = ["Alta Floresta D'Oeste, RO, Brazil",
               "Alto Alegre dos Parecis, RO, Brazil",
               "Alto Paraíso, RO, Brazil",
               "Alvorada D'Oeste, RO, Brazil",
               "Ariquemes, RO, Brazil",
               "Buritis, RO, Brazil",
               "Cabixi, RO, Brazil",
               "Cacaulândia, RO, Brazil",
               "Cacoal, RO, Brazil",
               "Campo Novo de Rondônia, RO, Brazil",
               "Candeias do Jamari, RO, Brazil",
               "Castanheiras, RO, Brazil",
               "Cerejeiras, RO, Brazil",
               "Chupinguaia, RO, Brazil",
               "Colorado do Oeste, RO, Brazil",
               "Corumbiara, RO, Brazil",
               "Costa Marques, RO, Brazil",
               "Cujubim, RO, Brazil",
               "Espigão D'Oeste, RO, Brazil",
               "Governador Jorge Teixeira, RO, Brazil",
               "Guajará-Mirim, RO, Brazil",
               "Itapuã do Oeste, RO, Brazil",
               "Jaru, RO, Brazil",
               "Ji-Paraná, RO, Brazil",
               "Machadinho D'Oeste, RO, Brazil",
               "Ministro Andreazza, RO, Brazil",
               "Mirante da Serra, RO, Brazil",
               "Monte Negro, RO, Brazil",
               "Nova Brasilândia D'Oeste, RO, Brazil",
               "Nova Mamoré, RO, Brazil",
               "Nova União, RO, Brazil",
               "Novo Horizonte do Oeste, RO, Brazil",
               "Ouro Preto do Oeste, RO, Brazil",
               "Parecis, RO, Brazil",
               "Pimenta Bueno, RO, Brazil",
               "Pimenteiras do Oeste, RO, Brazil",
               "Porto Velho, RO, Brazil",
               "Presidente Médici, RO, Brazil",
               "Primavera de Rondônia, RO, Brazil",
               "Rio Crespo, RO, Brazil",
               "Rolim de Moura, RO, Brazil",
               "Santa Luzia D'Oeste, RO, Brazil",
               "Seringueiras, RO, Brazil",
               "São Felipe D'Oeste, RO, Brazil",
               "São Francisco do Guaporé, RO, Brazil",
               "São Miguel do Guaporé, RO, Brazil",
               "Teixeirópolis, RO, Brazil",
               "Theobroma, RO, Brazil",
               "Urupá, RO, Brazil",
               "Vale do Anari, RO, Brazil",
               "Vale do Paraíso, RO, Brazil",
               "Vilhena, RO, Brazil"]
    
    distancias = []
    for c1 in cidades:
        print( c1 )
        dist = []
        for c2 in cidades:
            d = max( 5, round( distancia(c1, c2) * 1.3 ))
            dist.append(d)
        distancias.append(dist)

    print('\nMatriz completa:\n')
    
    for dist in distancias:
        print(dist)
