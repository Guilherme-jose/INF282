from math import factorial, exp


def rho(x, lmbda, mu):
    return lmbda / (x * mu)

def p_0(c, lmbda, mu):
    if rho(c, lmbda, mu) >= 1:
        return 0
    total = 0
    a = c * rho(c, lmbda, mu)
    for i in range(0, c):
        total += a ** i / factorial(i)
    total += a ** c / (factorial(c) * (1 - rho(c, lmbda, mu)))
    return 1 / total

def p_n(n, c, lmbda, mu):
    if rho(c, lmbda, mu) >= 1:
        return 0
    if (n < c):
        return ((c * rho(c, lmbda, mu)) ** n * p_0(c, lmbda, mu)) / factorial(n)
    else:
        return ((c * rho(c, lmbda, mu)) ** n * p_0(c, lmbda, mu)) / (factorial(c) * (c ** (n - c)))

def p_ge_c(c, lmbda, mu):
    if rho(c, lmbda, mu) >= 1:
        return 1

    a = c * rho(c, lmbda, mu)
    return (a ** c) * p_0(c, lmbda, mu) / (factorial(c) * (1 - rho(c, lmbda, mu)))

def L_q(c, lmbda, mu):
    if rho(c, lmbda, mu) >= 1:
        return float('inf')
    return p_ge_c(c, lmbda, mu) * rho(c, lmbda, mu) / (1 - rho(c, lmbda, mu))

def p_less_than_c(c, lmbda, mu):
    return 1 - p_ge_c(c, lmbda, mu)

def W_q(c, lmbda, mu):
    if rho(c, lmbda, mu) >= 1:
        return float('inf')
    return L_q(c, lmbda, mu) / lmbda

def p_W_q_equal_0(c, lmbda, mu):
    sum = 0 
    for n in range(0, c):
        sum += p_n(n, c, lmbda, mu)
    return sum

def p_W_q_greater_than_t(c, t, lmbda, mu):
    term_a = 1 - p_W_q_equal_0(c, lmbda, mu)
    term_b = exp(-c * mu * (1 - rho(c, lmbda, mu)) * t)
    return term_a * term_b

def c_s(c, p_s):
    return p_s * c

def c_q(c, p_q, lmbda, mu):
    return p_q *  L_q(c, lmbda, mu)

def c_total(c, lmbda, mu, p_s, p_q):
    return c_s(c, p_s) + c_q(c, p_q, lmbda, mu)
