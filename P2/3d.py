from mmc import *

lmbda = 4
mu = 60/27
c = range(1, 21)

print("c\tW_q")
for x in c:
    print(f"{x}\t{60 * 60 * W_q(x, lmbda, mu):.4f}")
