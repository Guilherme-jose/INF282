from mm1k import *

lmbda = 25
mu = 1/0.0037
rho = lmbda / mu

print("K\tp_0\tp_K\tL\tW_q")
for i in range(0, 21):
    print(f"{i}\t{p_n(0, i, lmbda, mu):.8f}\t{p_n(i, i, lmbda, mu):.8f}\t{L(i, lmbda, mu):.8f}\t{W_q(i, lmbda, mu):.8f}")

    import matplotlib.pyplot as plt

    
K_values = range(1, 21)
p_K_values = [p_n(i, i, lmbda, mu) for i in K_values]
one_minus_p_K = [1 - p for p in p_K_values]


plt.figure(figsize=(10, 6))
plt.yscale('log')
plt.ylim(bottom=0, top=1e25)
plt.yticks([1e2, 1e4, 1e6, 1e8, 1e10, 1e12, 1e14, 1e16, 1e18, 1e20, 1e22, 1e24], labels=[r'$10^{2}$', r'$10^{4}$', r'$10^{6}$', r'$10^{8}$', r'$10^{10}$', r'$10^{12}$', r'$10^{14}$', r'$10^{16}$', r'$10^{18}$', r'$10^{20}$', r'$10^{22}$', r'$10^{24}$'])
plt.xticks(K_values)

plt.plot(K_values, [(1 - v) / v for v in p_K_values], marker='o', label='(número de pacotes aceitos) / (número de pacotes perdidos)')
plt.xlabel('K')
plt.ylabel('Probability')
plt.legend()
plt.grid(True)
plt.show()