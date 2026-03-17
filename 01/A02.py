import numpy as np

import matplotlib.pyplot as plt

q = np.linspace(1, 100, 100)
K = 10.0  # Example value
D = 42.0  # Example value
h = 2.5   # Example value
t = np.linspace(0, 24, 2400)
r = 240.0
q_optimal = np.sqrt((2 * K * D) / h) * np.sqrt(r/(r - D))

plt.figure(figsize=(10, 6))
plt.plot(q, (h*q*(r-D))/(2*r), label='hq(r-D)/2r')
plt.plot(q, K*D/q, label='KD/q')
plt.plot(q, (h*q*(r-D))/(2*r) + K*D/q, label='TC\'(q) = KD/q + hq/2')
plt.xlabel('q')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()


import matplotlib.pyplot as plt
import numpy as np

# Parameters
D = 42
r = 240
q = 20.18

# Calculated Metrics
I_max = q * (1 - D/r)
t_prod = q / r          # Time spent producing
t_deplete = I_max / D   # Time spent depleting the max inventory
T_cycle = t_prod + t_deplete

def epq_inventory(t, D, r, q, I_max, T_cycle, t_prod):
    t_mod = t % T_cycle
    if t_mod <= t_prod:
        # Production Phase: Increasing at net rate (r - D)
        return (r - D) * t_mod
    else:
        # Depletion Phase: Decreasing from I_max at rate D
        return I_max - D * (t_mod - t_prod)

# Data Generation
t_vals = np.linspace(0, 1, 1000)
y_vals = [epq_inventory(t, D, r, q, I_max, T_cycle, t_prod) for t in t_vals]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(t_vals, y_vals, color='crimson', linewidth=2, label=f'EPQ Inventory (I_max={I_max:.2f})')

# Visual markers
plt.axhline(I_max, color='black', linestyle=':', alpha=0.5, label=f'I_max ({I_max:.2f})')
plt.axvline(t_prod, color='blue', linestyle='--', alpha=0.3, label='Production Ends')
plt.axvline(T_cycle, color='green', linestyle='--', alpha=0.3, label='Cycle Ends')

plt.title(f'EPQ Model: Max Inventory = q * (1 - D/r)\n(D={D}, r={r}, q={q})', fontsize=12)
plt.xlabel('Time')
plt.ylabel('Inventory Level')
plt.xlim(0, 1)
plt.ylim(0, I_max * 1.2)
plt.legend()
plt.grid(True, alpha=0.2)
plt.show()

print(f"Total Batch (q): {q}")
print(f"Peak Inventory (I_max): {I_max:.4f}")
print(f"Cycle Time (T): {T_cycle:.4f}")