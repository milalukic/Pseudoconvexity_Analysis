import numpy as np
import sympy as sp

from calculating_grad import evaluate_expression
from interval_matrix import IntervalMatrix, Interval
from tests_unofficial import f1, f_der1, f_der2, f2, f2_der1, f2_der2

# Computing the hessian matrix and gradients from a function 
def compute_hessian(f, symbols):
    hessian_matrix = sp.hessian(f, symbols)
    return hessian_matrix

def compute_gradient(f, symbols):
    gradient = []
    for symbol in symbols:
        gradient.append(sp.diff(f, symbol))
    return sp.Matrix(gradient)

def make_gradient_matrix(g):
    g_matrix = g * g.T
    # Expand each element of the matrix
    g_matrix_expanded = g_matrix.applyfunc(sp.expand)
    return g_matrix_expanded

def compute_M(H, g, intervals, symbols, alpha=1.0):
    # M_alpha = H + alpha*g*g^T - actual formula to calculate M
    g_matrix = make_gradient_matrix(g)
    M = H + alpha*g_matrix

    M_eval = []
    for expression in M:
        result = evaluate_expression(str(expression), intervals, symbols)
        M_eval.append(result)

    return IntervalMatrix(M_eval)

def first_condition(M):
    # min_ev = smallest eingenvalue of M_alpha_c
    min_evc = min(np.linalg.eigvals(M.calculateMidpoint()))
    # spectral_radius = max eingenvalue of M_alpha_delta
    max_evd = max(np.linalg.eigvals(M.calculateRadius()))
    if min_evc >= max_evd:
        return True
    return False

def second_condition(M):
    # M_alpha_c - M_alpha_delta*diag(z) is positive semidefinite for every z={+-1}^n-1 x {1}
    Mc = M.calculateMidpoint()
    Md = M.calculateRadius()
    z = np.diag([1 for _ in range(M.rows)])
    
    M_combined = Mc - np.dot(Md, z)
    print(M_combined)

    # positive semidefinite = all eigvals >= 0
    return np.all(np.linalg.eigvals(M_combined) >= 0)