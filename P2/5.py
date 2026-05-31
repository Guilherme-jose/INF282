from mmc import *

lmbda = 60
mu = 60 / 21

c = range(20, 31)

print("c\tp_<c\tW_q")

for x in c:
    print(f"{x}\t{p_less_than_c(x, lmbda, mu):.4f}\t{60 * W_q(x, lmbda, mu):.4f}")