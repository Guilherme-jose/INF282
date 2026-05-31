from mmc import *

lmbda = 200
mu = 25
c = range(9, 20)

p_q = 25
p_s = 3.40

print("c\tp_0\tp_ge_c\tL_q\tc_s\tc_q\tc_total")
for x in c:
    print(f"{x}\t{p_0(x, lmbda, mu):.4f}\t{p_ge_c(x, lmbda, mu):.4f}\t{L_q(x, lmbda, mu):.4f}\t{c_s(x, p_s):.2f}\t{c_q(x, p_q, lmbda, mu):.2f}\t{c_total(x, lmbda, mu, p_s, p_q):.2f}")


import matplotlib.pyplot as plt

c_values = list(c)
c_s_values = [c_s(x, p_s) for x in c_values]
c_q_values = [c_q(x, p_q, lmbda, mu) for x in c_values]
c_total_values = [c_total(x, lmbda, mu, p_s, p_q) for x in c_values]


plt.figure(figsize=(10, 6))
plt.xticks(c_values)
plt.xlim(left=c_values[0] - 1)
plt.ylim(bottom=0, top=max(c_total_values) * 1.1)
plt.plot(c_values, c_s_values, label='c_s', marker='o')
plt.plot(c_values, c_q_values, label='c_q', marker='s')
plt.plot(c_values, c_total_values, label='c_total', marker='^')
plt.xlabel('c')
plt.ylabel('Cost')
plt.legend()
plt.grid(True)
plt.show()