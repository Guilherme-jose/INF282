from mmc import *

lmbda = 4
mu = 60/27
c = range(1, 21)

print("c\tP_W_q_>2")
for x in c:
    print(f"{x}\t{p_W_q_greater_than_t(x, 2/60, lmbda, mu):.4f}")