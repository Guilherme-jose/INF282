# M/M/1 queueing system


def p_n(n, lmbda, mu):
    rho = lmbda / mu
    return (1 - rho) * rho**n

def p_less_than_n(n, lmbda, mu):
    rho = lmbda / mu
    return 1 - rho**n

def W_q(lmbda, mu):
    rho = lmbda / mu
    if rho >= 1:
        return float('inf')
    return rho / (mu * (1 - rho))






