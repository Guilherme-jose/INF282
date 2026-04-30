from math import factorial

lmbda = 200
mu = 25


p_q = 25
p_s = 3.40

c = range(9, 20)

def rho(x):
    return lmbda / (x * mu)

def p_0(x):
    if rho(x) >= 1:
        return 0
    total = 0
    a = x * rho(x)
    for i in range(0, x):
        total += a ** i / factorial(i)
    total += a ** x / (factorial(x) * (1 - rho(x)))
    return 1 / total

def p_ge_c(x):
    if rho(x) >= 1:
        return 1

    a = x * rho(x)
    return (a ** x) * p_0(x) / (factorial(x) * (1 - rho(x)))

def L_q(x):
    if rho(x) >= 1:
        return float('inf')
    return p_ge_c(x) * rho(x) / (1 - rho(x))


def c_s(x):
    return p_s * x

def c_q(x):
    return p_q *  L_q(x)

def c_total(x):
    return c_s(x) + c_q(x)

print("c\tp_0\tp_ge_c\tL_q\tc_s\tc_q\tc_total")
for x in c:
    print(f"{x}\t{p_0(x):.4f}\t{p_ge_c(x):.4f}\t{L_q(x):.4f}\t{c_s(x):.2f}\t{c_q(x):.2f}\t{c_total(x):.2f}")


import matplotlib.pyplot as plt

c_values = list(c)
c_s_values = [c_s(x) for x in c_values]
c_q_values = [c_q(x) for x in c_values]
c_total_values = [c_total(x) for x in c_values]

plt.figure(figsize=(10, 6))
plt.plot(c_values, c_s_values, label='c_s', marker='o')
plt.plot(c_values, c_q_values, label='c_q', marker='s')
plt.plot(c_values, c_total_values, label='c_total', marker='^')
plt.xlabel('c')
plt.ylabel('Cost')
plt.legend()
plt.grid(True)
plt.show()