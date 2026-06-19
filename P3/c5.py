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

distances = [   5, 506, 224, 845, 372, 626, 799, 296, 360, 295, 342, 576, 302, 590, 454, 490, 275, 160, 406, 358, 208, 552, 305, 210, 174, 
506,   5, 284, 346, 137, 127, 300, 330, 297, 212, 231, 515, 337,  89, 125, 128, 310, 532, 171, 169, 365,  51, 247, 345, 593, 
224, 284,   5, 623, 150, 404, 577, 112, 177,  73, 120, 392, 119, 368, 232, 268,  92, 250, 184, 136,  97, 330,  82,  67, 311, 
845, 346, 623,   5, 476, 223,  45, 670, 635, 551, 569, 440, 676, 435, 464, 509, 648, 871, 509, 507, 704, 392, 586, 684, 931, 
372, 137, 150, 476,   5, 257, 430, 196, 162,  78,  96, 381, 203, 221,  85, 121, 175, 397,  37,  34, 231, 183, 113, 211, 458, 
626, 127, 404, 223, 257,   5, 177, 451, 417, 333, 351, 636, 458, 212, 246, 291, 430, 652, 291, 289, 486, 174, 367, 465, 713, 
799, 300, 577,  45, 430, 177,   5, 624, 590, 506, 524, 485, 630, 389, 419, 464, 603, 825, 464, 462, 659, 347, 540, 638, 886, 
296, 330, 112, 670, 196, 451, 624,   5, 113, 120, 108, 328,  44, 415, 278, 315,  27, 321, 230, 167,  88, 377,  61, 108, 382, 
360, 297, 177, 635, 162, 417, 590, 113,   5, 122,  69, 219, 165, 381, 244, 281,  89, 386, 197, 128, 193, 343, 103, 173, 447, 
295, 212,  73, 551,  78, 333, 506, 120, 122,   5,  54, 341, 126, 297, 160, 197,  99, 321, 112,  90, 154, 258,  36, 134, 382, 
342, 231, 120, 569,  96, 351, 524, 108,  69,  54,   5, 288, 173, 315, 178, 215,  85, 368, 130,  62, 201, 277,  67, 181, 428, 
576, 515, 392, 440, 381, 636, 485, 328, 219, 341, 288,   5, 380, 600, 463, 500, 304, 601, 415, 347, 408, 562, 322, 388, 662, 
302, 337, 119, 676, 203, 458, 630,  44, 165, 126, 173, 380,   5, 422, 285, 322,  79, 216, 237, 189,  37, 383, 110, 114, 278, 
590,  89, 368, 435, 221, 212, 389, 415, 381, 297, 315, 600, 422,   5, 210, 213, 394, 616, 255, 253, 450,  84, 331, 429, 677, 
454, 125, 232, 464,  85, 246, 419, 278, 244, 160, 178, 463, 285, 210,   5, 118, 258, 480, 118, 116, 313, 171, 194, 293, 540, 
490, 128, 268, 509, 121, 291, 464, 315, 281, 197, 215, 500, 322, 213, 118,   5, 294, 516,  91, 153, 349, 131, 231, 329, 577, 
275, 310,  92, 648, 175, 430, 603,  27,  89,  99,  85, 304,  79, 394, 258, 294,   5, 300, 210, 144, 107, 356,  34,  87, 361, 
160, 532, 250, 871, 397, 652, 825, 321, 386, 321, 368, 601, 216, 616, 480, 516, 300,   5, 432, 384, 181, 578, 331, 236,  61, 
406, 171, 184, 509,  37, 291, 464, 230, 197, 112, 130, 415, 237, 255, 118,  91, 210, 432,   5,  68, 265, 217, 147, 245, 493, 
358, 169, 136, 507,  34, 289, 462, 167, 128,  90,  62, 347, 189, 253, 116, 153, 144, 384,  68,   5, 217, 215,  93, 197, 445, 
208, 365,  97, 704, 231, 486, 659,  88, 193, 154, 201, 408,  37, 450, 313, 349, 107, 181, 265, 217,   5, 411, 138,  71, 243, 
552,  51, 330, 392, 183, 174, 347, 377, 343, 258, 277, 562, 383,  84, 171, 131, 356, 578, 217, 215, 411,   5, 293, 391, 639, 
305, 247,  82, 586, 113, 367, 540,  61, 103,  36,  67, 322, 110, 331, 194, 231,  34, 331, 147,  93, 138, 293,   5, 117, 392, 
210, 345,  67, 684, 211, 465, 638, 108, 173, 134, 181, 388, 114, 429, 293, 329,  87, 236, 245, 197,  71, 391, 117,   5, 297, 
174, 593, 311, 931, 458, 713, 886, 382, 447, 382, 428, 662, 278, 677, 540, 577, 361,  61, 493, 445, 243, 639, 392, 297,   5 ]

num_cities = len(cities)
num_psas = 9

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

#numero de PSAs limitados
prob += lpSum(y[j] for j in range(num_cities)) == num_psas

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