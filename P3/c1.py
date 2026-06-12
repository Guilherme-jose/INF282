from pulp import *
import pandas as pd
import time

rondonia_populacao = {
    "Porto Velho": 517709,
    "Ji-Paraná": 140101,
    "Vilhena": 109651,
    "Ariquemes": 109170,
    "Cacoal": 98280,
    "Rolim de Moura": 62959,
    "Jaru": 55682,
    "Guajará-Mirim": 43594,
    "Pimenta Bueno": 39220,
    "Ouro Preto do Oeste": 38684,
    "Machadinho d'Oeste": 34149,
    "Espigão d'Oeste": 32842,
    "Buritis": 30649,
    "Nova Mamoré": 28701,
    "Candeias do Jamari": 24313,
    "Alta Floresta d'Oeste": 22787,
    "São Miguel do Guaporé": 22305,
    "Presidente Médici": 20443,
    "São Francisco do Guaporé": 17557,
    "Alto Paraíso": 17467,
    "Cerejeiras": 16966,
    "Colorado do Oeste": 16508,
    "Nova Brasilândia d'Oeste": 16374,
    "Cujubim": 15877,
    "Alvorada d'Oeste": 13720,
    "Costa Marques": 13510,
    "Seringueiras": 12965,
    "Alto Alegre dos Parecis": 12237,
    "Monte Negro": 12168,
    "Urupá": 11314,
    "Chupinguaia": 10191,
    "Mirante da Serra": 9657,
    "Itapuã do Oeste": 9228,
    "Campo Novo de Rondônia": 9095,
    "Theobroma": 8459,
    "Governador Jorge Teixeira": 8340,
    "Vale do Anari": 8220,
    "Novo Horizonte do Oeste": 7972,
    "Corumbiara": 7968,
    "Santa Luzia d'Oeste": 7837,
    "Vale do Paraíso": 6790,
    "Nova União": 6541,
    "Ministro Andreazza": 6519,
    "Cabixi": 5664,
    "São Felipe d'Oeste": 5588,
    "Teixeirópolis": 4521,
    "Parecis": 4372,
    "Cacaulândia": 4292,
    "Rio Crespo": 3767,
    "Castanheiras": 3450,
    "Primavera de Rondônia": 3268,
    "Pimenteiras do Oeste": 2309
}



c_t = 0.35
f = 500000

df = pd.read_csv('/home/guilherme/INF282/P3/dist_rondonia.csv')

cities = sorted(df['orig'].unique().tolist())
demands = [rondonia_populacao[city] * 0.2 for city in cities]

distances = []
for orig in cities:
    for dest in cities:
        dist = df[(df['orig'] == orig) & (df['dest'] == dest)]['dist'].values
        if len(dist) > 0:
            distances.append(dist[0])
        else:
            # Use symmetric distance if not found
            dist = df[(df['orig'] == dest) & (df['dest'] == orig)]['dist'].values
            distances.append(dist[0] if len(dist) > 0 else 0)

num_customers = len(cities)
num_facilities = len(cities)


transport_cost = [[(distances[i * num_facilities + j] * c_t * 2) for j in range(num_facilities)] for i in range(num_customers)]
facility_cost = [f] * num_facilities
facility_capacity = [1e9] * num_facilities
customer_demand = demands


# Create model
prob = LpProblem("Facility_Placement", LpMinimize)

# Decision variables
x = [[LpVariable(f"transport_{i}_{j}", lowBound=0, upBound=1) for j in range(num_facilities)] 
     for i in range(num_customers)]
y = [LpVariable(f"facility_{j}", cat='Binary') for j in range(num_facilities)]

# Objective function
prob += lpSum([transport_cost[i][j] * x[i][j] * customer_demand[i] for i in range(num_customers) for j in range(num_facilities)]) + \
        lpSum([facility_cost[j] * y[j] for j in range(num_facilities)])

# Demand constraints
for i in range(num_customers):
    prob += lpSum([x[i][j] for j in range(num_facilities)]) == 1

# Capacity constraints
for j in range(num_facilities):
    prob += lpSum([x[i][j] * customer_demand[i] for i in range(num_customers)]) <= facility_capacity[j] * y[j]

# Solve
prob.solve()

print(f"Status: {LpStatus[prob.status]}")
print(f"Total Cost: {value(prob.objective)}")

for j in range(num_facilities):
    for i in range(num_customers):
        if x[i][j].varValue > 0:
            print(f"  Percentage from Facility {j} to Customer {i}: {x[i][j].varValue}")

# Print formatted results
print("\n" + "="*50)
print(f"Status do modelo: {LpStatus[prob.status]}")
print("="*50)

# Calculate costs
fixed_cost = sum(facility_cost[j] * y[j].varValue for j in range(num_facilities))
transport_cost_total = sum(transport_cost[i][j] * x[i][j].varValue * customer_demand[i] 
                            for i in range(num_customers) for j in range(num_facilities))

print(f"Custo fixo dos PSAs:             {fixed_cost:,.2f}")
print(f"Custo de Transporte p/ PSAs:     {transport_cost_total:,.2f}")
print(f"Custo total:                     {value(prob.objective):,.2f}")

# Active facilities
active_facilities = [j for j in range(num_facilities) if y[j].varValue > 0.5]
print(f"\nCidades com PSAs: ")
for idx, j in enumerate(active_facilities, 1):
    print(f" {idx}. {cities[j]}")

# Transportation table
print(f"\nQuantidades transportadas das cidades p/ os PSAs:\n")
print(f"{'Origem':<30} {'Destino':<30} {'Qtde':>10}")
print("-"*72)
for i in range(num_customers):
    for j in range(num_facilities):
        if x[i][j].varValue > 0:
            qty = x[i][j].varValue * customer_demand[i]
            print(f"{cities[i]:<30} {cities[j]:<30} {qty:>10.0f}")

# Summary by facility
print(f"\nCidades atendidas por cada PSA:\n")
for j in active_facilities:
    print(f"{'PSA':<30} {'Cidade Atendida':<30} {'Qtde':>10}")
    print("-"*72)
    total_facility = 0
    for i in range(num_customers):
        if x[i][j].varValue > 0:
            qty = x[i][j].varValue * customer_demand[i]
            print(f"{cities[j]:<30} {cities[i]:<30} {qty:>10.0f}")
            total_facility += qty
    print(f"{'Total:':<30} {'':<30} {total_facility:>10.0f}")
    print("-"*72)