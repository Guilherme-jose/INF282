from pulp import *

# Facility Placement Problem using PuLP

# Data
num_customers = 3
num_facilities = 3
customer_demand = [7, 7, 7]
facility_capacity = [12, 12, 12]
transport_cost = [
    [3, 1e10, 1e10],
    [5, 6, 2],
    [9, 7, 3]
]

facility_cost = [50, 60, 58]

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