from mmc import *

lmbda = 4
mu = 60/27
c = 3

print("W_q =", 60 * W_q(c, lmbda, mu))
print("p_>6 =", 1 - (p_n(6, c, lmbda, mu) + p_n(5, c, lmbda, mu) + p_n(4, c, lmbda, mu) + p_n(3, c, lmbda, mu) + p_n(2, c, lmbda, mu) + p_n(1, c, lmbda, mu) + p_n(0, c, lmbda, mu)))