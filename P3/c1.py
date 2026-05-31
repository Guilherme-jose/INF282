from pulp import *

demands = []

cities = list(map(str.strip, """Porto Velho
Ji-Paraná
Vilhena
Ariquemes
Cacoal
Rolim de Moura
Jaru
Guajará-Mirim
Pimenta Bueno
Ouro Preto do Oeste
Machadinho d'Oeste
Espigão d'Oeste
Buritis
Nova Mamoré
Candeias do Jamari
Alta Floresta d'Oeste
São Miguel do Guaporé
Presidente Médici
São Francisco do Guaporé
Alto Paraíso
Cerejeiras
Colorado do Oeste
Nova Brasilândia d'Oeste
Cujubim
Alvorada d'Oeste
Costa Marques
Seringueiras
Alto Alegre dos Parecis
Monte Negro
Urupá
Chupinguaia
Mirante da Serra
Itapuã do Oeste
Campo Novo de Rondônia
Theobroma
Governador Jorge Teixeira
Vale do Anari
Novo Horizonte do Oeste
Corumbiara
Santa Luzia d'Oeste
Vale do Paraíso
Nova União
Ministro Andreazza
Cabixi
São Felipe d'Oeste
Teixeirópolis
Parecis
Cacaulândia
Rio Crespo
Castanheiras
Primavera de Rondônia
Pimenteiras do Oeste""".split('\n')))

demands = [517709, 140101, 109651, 109170, 98280, 62959, 55682, 43594, 39220, 38684, 34149, 32842, 30649, 28701, 24313, 22787, 22305, 20443, 17557, 17467, 16966, 16508, 16374, 15877, 13720, 13510, 12965, 12237, 12168, 11314, 10191, 9657, 9228, 9095, 8459, 8340, 8220, 7972, 7968, 7837, 6790, 6541, 6519, 5664, 5588, 4521, 4372, 4292, 3767, 3450, 3268, 2309]
demands = [d * 0.2 for d in demands]

c_t = 0.35
f = 500000


num_customers = len(cities)
num_facilities = len(cities)
transport_cost = [[(distances[i * num_facilities + j] * c_t) for j in range(num_facilities)] for i in range(num_customers)]
facility_cost = [f] * num_facilities
facility_capacity = [max(demands) * 1.5] * num_facilities
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
    print(f"Facility {j} Open: {y[j].varValue}")
    for i in range(num_customers):
        print(f"  Percentage from Facility {j} to Customer {i}: {x[i][j].varValue}")