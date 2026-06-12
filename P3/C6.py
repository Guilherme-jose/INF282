from pulp import *
import pandas as pd
import time

cities = ["Vilhena", "Ariquemes", "Cacoal", "Guajará-Mirim", "Ouro Preto do Oeste", 
        "Buritis", "Nova Mamoré", "Alta Floresta D'Oeste", "São Miguel do Guaporé", 
        "Presidente Médici", "Alvorada D'Oeste", "Costa Marques", "Alto Alegre dos Parecis", 
        "Itapuã do Oeste", "Governador Jorge Teixeira", "Vale do Anari", "Novo Horizonte do Oeste", 
        "Corumbiara", "Vale do Paraíso", "Teixeirópolis", "Parecis", "Rio Crespo", 
        "Castanheiras", "Primavera de Rondônia", "Pimenteiras do Oeste"]

pop = [109651, 109170, 98280, 43594, 38684, 30649, 28701, 22787, 22305, 20443, 13720, 13510, 12237, 9228, 8340, 8220, 7972, 7968, 6790, 4521, 4372, 3767, 3450, 3268, 2309]

c_t = 0.35
f_psa = 500000
f_hosp = 2000000  # Custo anual do hospital (R$ 2 milhões)

# df = pd.read_csv('/home/guilherme/INF282/P3/dist_rondonia.csv') # Mantido caso precise

demands = [pop[i] * 0.2 for i in range(len(cities))]

distances = [   5,  44, 108, 330, 451, 112,  61, 321, 328, 278, 670, 415, 624,  27, 196,  88, 382, 120, 108, 377, 113, 167, 315, 230, 296, 
 44,   5, 173, 337, 458, 119, 110, 216, 380, 285, 676, 422, 630,  79, 203,  37, 278, 126, 114, 383, 165, 189, 322, 237, 302, 
108, 173,   5, 231, 351, 120,  67, 368, 288, 178, 569, 315, 524,  85,  96, 201, 428,  54, 181, 277,  69,  62, 215, 130, 342, 
330, 337, 231,   5, 127, 284, 247, 532, 515, 125, 346,  89, 300, 310, 137, 365, 593, 212, 345,  51, 297, 169, 128, 171, 506, 
451, 458, 351, 127,   5, 404, 367, 652, 636, 246, 223, 212, 177, 430, 257, 486, 713, 333, 465, 174, 417, 289, 291, 291, 626, 
112, 119, 120, 284, 404,   5,  82, 250, 392, 232, 623, 368, 577,  92, 150,  97, 311,  73,  67, 330, 177, 136, 268, 184, 224, 
 61, 110,  67, 247, 367,  82,   5, 331, 322, 194, 586, 331, 540,  34, 113, 138, 392,  36, 117, 293, 103,  93, 231, 147, 305, 
321, 216, 368, 532, 652, 250, 331,   5, 601, 480, 871, 616, 825, 300, 397, 181,  61, 321, 236, 578, 386, 384, 516, 432, 160, 
328, 380, 288, 515, 636, 392, 322, 601,   5, 463, 440, 600, 485, 304, 381, 408, 662, 341, 388, 562, 219, 347, 500, 415, 576, 
278, 285, 178, 125, 246, 232, 194, 480, 463,   5, 464, 210, 419, 258,  85, 313, 540, 160, 293, 171, 244, 116, 118, 118, 454, 
670, 676, 569, 346, 223, 623, 586, 871, 440, 464,   5, 435,  45, 648, 476, 704, 931, 551, 684, 392, 635, 507, 509, 509, 845, 
415, 422, 315,  89, 212, 368, 331, 616, 600, 210, 435,   5, 389, 394, 221, 450, 677, 297, 429,  84, 381, 253, 213, 255, 590, 
624, 630, 524, 300, 177, 577, 540, 825, 485, 419,  45, 389,   5, 603, 430, 659, 886, 506, 638, 347, 590, 462, 464, 464, 799, 
 27,  79,  85, 310, 430,  92,  34, 300, 304, 258, 648, 394, 603,   5, 175, 107, 361,  99,  87, 356,  89, 144, 294, 210, 275, 
196, 203,  96, 137, 257, 150, 113, 397, 381,  85, 476, 221, 430, 175,   5, 231, 458,  78, 211, 183, 162,  34, 121,  37, 372, 
 88,  37, 201, 365, 486,  97, 138, 181, 408, 313, 704, 450, 659, 107, 231,   5, 243, 154,  71, 411, 193, 217, 349, 265, 208, 
382, 278, 428, 593, 713, 311, 392,  61, 662, 540, 931, 677, 886, 361, 458, 243,   5, 382, 297, 639, 447, 445, 577, 493, 174, 
120, 126,  54, 212, 333,  73,  36, 321, 341, 160, 551, 297, 506,  99,  78, 154, 382,   5, 134, 258, 122,  90, 197, 112, 295, 
108, 114, 181, 345, 465,  67, 117, 236, 388, 293, 684, 429, 638,  87, 211,  71, 297, 134,   5, 391, 173, 197, 329, 245, 210, 
377, 383, 277,  51, 174, 330, 293, 578, 562, 171, 392,  84, 347, 356, 183, 411, 639, 258, 391,   5, 343, 215, 131, 217, 552, 
113, 165,  69, 297, 417, 177, 103, 386, 219, 244, 635, 381, 590,  89, 162, 193, 447, 122, 173, 343,   5, 128, 281, 197, 360, 
167, 189,  62, 169, 289, 136,  93, 384, 347, 116, 507, 253, 462, 144,  34, 217, 445,  90, 197, 215, 128,   5, 153,  68, 358, 
315, 322, 215, 128, 291, 268, 231, 516, 500, 118, 509, 213, 464, 294, 121, 349, 577, 197, 329, 131, 281, 153,   5,  91, 490, 
230, 237, 130, 171, 291, 184, 147, 432, 415, 118, 509, 255, 464, 210,  37, 265, 493, 112, 245, 217, 197,  68,  91,   5, 406, 
296, 302, 342, 506, 626, 224, 305, 160, 576, 454, 845, 590, 799, 275, 372, 208, 174, 295, 210, 552, 360, 358, 490, 406,   5 ]

num_cities = len(cities)

# Matrizes de custo de transporte
# 1. Cidade para PSA: 100% ida, 90% volta -> fator 1.9
transport_cost_psa = [[(distances[i * num_cities + j] * c_t * 1.9) for j in range(num_cities)] for i in range(num_cities)]

# 2. PSA para Hospital: Apenas ida -> fator 1.0. O fluxo real (10%) será controlado na variável de fluxo continuo.
transport_cost_hosp = [[(distances[j * num_cities + k] * c_t * 1.0) for k in range(num_cities)] for j in range(num_cities)]

facility_cost_psa = [f_psa] * num_cities
facility_cost_hosp = [f_hosp] * num_cities
facility_capacity = [22000] * num_cities
customer_demand = demands

# Criar modelo
prob = LpProblem("Multi_Echelon_Healthcare_Placement", LpMinimize)

# Variáveis de Decisão
x = [[LpVariable(f"transport_city_{i}_psa_{j}", cat='Binary') for j in range(num_cities)] for i in range(num_cities)]
y = [LpVariable(f"facility_psa_{j}", cat='Binary') for j in range(num_cities)]
z = [LpVariable(f"facility_hosp_{k}", cat='Binary') for k in range(num_cities)]

# Fluxo contínuo de pacientes do PSA j para o Hospital k (representando os 10%)
F = [[LpVariable(f"flow_psa_{j}_hosp_{k}", lowBound=0, cat='Continuous') for k in range(num_cities)] for j in range(num_cities)]

# Função Objetivo
prob += (
    lpSum([transport_cost_psa[i][j] * x[i][j] * customer_demand[i] for i in range(num_cities) for j in range(num_cities)]) +
    lpSum([transport_cost_hosp[j][k] * F[j][k] for j in range(num_cities) for k in range(num_cities)]) +
    lpSum([facility_cost_psa[j] * y[j] for j in range(num_cities)]) +
    lpSum([facility_cost_hosp[k] * z[k] for k in range(num_cities)])
)

# --- Restrições ---

# 1. Cada cidade deve ser atendida por exatamente um PSA
for i in range(num_cities):
    prob += lpSum([x[i][j] for j in range(num_cities)]) == 1

# 2. Capacidade dos PSAs e ativação do PSA j
for j in range(num_cities):
    prob += lpSum([x[i][j] * customer_demand[i] for i in range(num_cities)]) <= facility_capacity[j] * y[j]

# 3. Conservação de fluxo: 10% de toda a demanda que chega no PSA j deve ir para algum hospital k
for j in range(num_cities):
    prob += lpSum([F[j][k] for k in range(num_cities)]) == 0.10 * lpSum([x[i][j] * customer_demand[i] for i in range(num_cities)])

# 4. Ativação do Hospital k (Se houver fluxo para o hospital k, ele deve estar aberto)
# O fluxo máximo total possível para todos os hospitais juntos é 10% da demanda total do estado
max_total_hosp_flow = 0.10 * sum(customer_demand)
for k in range(num_cities):
    prob += lpSum([F[j][k] for j in range(num_cities)]) <= max_total_hosp_flow * z[k]

# Only a psa OR a hospital can be open in each city
for j in range(num_cities):
    prob += y[j] + z[j] <= 1

# Resolver
prob.solve()

# --- Print formatado dos resultados ---
print("\n" + "="*60)
print(f"Status do modelo: {LpStatus[prob.status]}")
print("="*60)

# Cálculo detalhado dos custos
fixed_cost_psa_total = sum(facility_cost_psa[j] * y[j].varValue for j in range(num_cities))
fixed_cost_hosp_total = sum(facility_cost_hosp[k] * z[k].varValue for k in range(num_cities))

trans_cost_psa_total = sum(transport_cost_psa[i][j] * x[i][j].varValue * customer_demand[i] 
                           for i in range(num_cities) for j in range(num_cities))

trans_cost_hosp_total = sum(transport_cost_hosp[j][k] * F[j][k].varValue 
                            for j in range(num_cities) for k in range(num_cities))

print(f"Custo Fixo dos PSAs:              R$ {fixed_cost_psa_total:,.2f}")
print(f"Custo Fixo dos Hospitais:         R$ {fixed_cost_hosp_total:,.2f}")
print(f"Custo de Transporte (Cidades->PSA): R$ {trans_cost_psa_total:,.2f}")
print(f"Custo de Transporte (PSA->Hosp):   R$ {trans_cost_hosp_total:,.2f}")
print("-" * 60)
print(f"CUSTO TOTAL DO SISTEMA:           R$ {value(prob.objective):,.2f}")
print("="*60)

# PSAs Ativos
active_psas = [j for j in range(num_cities) if y[j].varValue > 0.5]
print(f"\nCidades com PSAs ativos ({len(active_psas)}):")
for idx, j in enumerate(active_psas, 1):
    print(f"  {idx}. {cities[j]}")

# Hospitais Ativos
active_hosps = [k for k in range(num_cities) if z[k].varValue > 0.5]
print(f"\nCidades com Hospitais ativos ({len(active_hosps)}):")
for idx, k in enumerate(active_hosps, 1):
    print(f"  {idx}. {cities[k]}")

# Fluxo PSA -> Hospital
print(f"\nFluxo de pacientes dos PSAs para os Hospitais (10%):")
print(f"{'PSA Origem':<25} {'Hospital Destino':<25} {'Pacientes/Ano':>15}")
print("-"*68)
for j in range(num_cities):
    for k in range(num_cities):
        if F[j][k].varValue > 0.01:
            print(f"{cities[j]:<25} {cities[k]:<25} {F[j][k].varValue:>15.1f}")