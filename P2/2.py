from mm1 import *

lmbda = 3
mu = 1/0.17

n = range(0, 21)

print("n\tP_<=n")
for x in n:
    print(f"{x}\t{p_n(x, lmbda, mu) + p_less_than_n(x, lmbda, mu):.4f}")