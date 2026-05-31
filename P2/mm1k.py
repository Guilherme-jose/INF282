#M/M/1/K queueing system



def p_n(n, K, lmbda, mu):
    rho = lmbda / mu
    return rho ** n * (1 - rho) / (1 - rho ** (K + 1))

def n_r(K, lmbda, mu):
    return lmbda * p_n(K, K, lmbda, mu)

def L(K, lmbda, mu):
    rho = lmbda / mu
    term_a = (1 - (K + 1) * rho ** K + K * rho ** (K + 1))
    term_b = (1 - rho) * (1 - rho ** (K + 1))
    return (rho * term_a) / term_b

def L_q(K, lmbda, mu):
    return L(K, lmbda, mu) - (1 - p_n(0, K, lmbda, mu))

def W_q(K, lmbda, mu):
    if (1 - p_n(K, K, lmbda, mu)) == 0:
        return float('inf')  # Avoid division by zero
    return L_q(K, lmbda, mu) / (lmbda * (1 - p_n(K, K, lmbda, mu)))
