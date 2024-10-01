import math
import scipy.special as special
import sympy as sp

# # Function 1 EXAMPLE f(x, y) = x^2 + y^2 - Will be generalized later
# def f1(x, y):
#     return x**2 + y**2

# # Function 2 EXAMPLE f(x, y) = ln(1 + x^2 + y^2)
# def f2(x, y):
#     return  x**2 + x*y + y**2

# # function 3:
# def f3(x, y):
#     return -x**2 + y
    
def normal(x, mean, std_dev):
    coefficient = 1 / (std_dev * math.sqrt(2 * math.pi))
    power = -((x - mean) ** 2) / (2 * std_dev ** 2)
    exponent = math.e**power
    return coefficient * exponent

def beta(x, alpha, beta):
    # Beta function B(alpha, beta)
    B = special.beta(alpha, beta)
    return (x**(alpha - 1) * (1 - x)**(beta - 1)) / B

def gamma(x, k, theta):
    # Gamma function Γ(k)
    gamma_const = special.gamma(k)
    return (x**(k-1) * math.e**(-x/theta)) / (theta**k * gamma_const)    

def exponential(x, lam):
    return lam*math.e**(-lam*x)