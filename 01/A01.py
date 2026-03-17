import numpy as np

import matplotlib.pyplot as plt

q = np.linspace(1, 100, 100)
K = 120.0  # Example value
D = 250.0  # Example value
h = 55.0   # Example value
t = np.linspace(0, 30, 3000)
q_optimal = np.sqrt((2 * K * D) / h)

plt.figure(figsize=(10, 6))
plt.plot(q, (K * D)/q, label='KD/q')
plt.plot(q, (h * q)/2, label='hq/2')
plt.plot(q, (K * D)/q + (h * q)/2, label='TC(q) = KD/q + hq/2')
plt.xlabel('q')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(t, q_optimal - q_optimal * (t % (30 * q_optimal / D))/(30 * q_optimal / D), label='I(q)') 
plt.xlabel('t')
plt.ylabel('Inventory')
plt.legend()
plt.grid(True)
plt.show()

q = np.linspace(1, 100)
K = 120.0  # Example value
D = 200.0  # Example value
h = 30.0   # Example value
q_optimal = np.sqrt((2 * K * D) / h)

plt.figure(figsize=(10, 6))
plt.plot(q, (K * D)/q, label='KD/q')
plt.plot(q, (h * q)/2, label='hq/2')
plt.plot(q, (K * D)/q + (h * q)/2, label='TC(q) = KD/q + hq/2')
plt.xlabel('q')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(t, q_optimal - q_optimal * (t % (30 * q_optimal / D))/(30 * q_optimal / D), label='I(q)') 
plt.xlabel('t')
plt.ylabel('Inventory')
plt.legend()
plt.grid(True)
plt.show()