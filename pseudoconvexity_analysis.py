import numpy as np
import sympy as sp

from calculating_grad import evaluate_expression
from interval_matrix import IntervalMatrix, Interval
from tests_unofficial import f1, f_der1, f_der2, f2, f2_der1, f2_der2

def compute_hessian(f, symbols):
    # Compute the Hessian matrix of a function.
    return sp.hessian(f, symbols)

def compute_gradient(f, symbols):
    # Compute the gradient vector of a function.
    gradient = [sp.diff(f, symbol) for symbol in symbols]
    return sp.Matrix(gradient)

def make_gradient_matrix(g):
    g_matrix = g * g.T
    # Expand each element of the matrix
    g_matrix_expanded = g_matrix.applyfunc(sp.expand)
    return g_matrix_expanded

def compute_M(H, g, intervals, symbols, alpha=1.0):
    # Compute the matrix M_alpha using Hessian H, gradient g, and scalar alpha.
    g_matrix = make_gradient_matrix(g)
    M = H + alpha * g_matrix

    M_eval = [evaluate_expression(str(expr), intervals, symbols) for expr in M]
    return IntervalMatrix(M_eval)

def first_condition(M):
    # Check if the smallest eigenvalue of M_alpha_c is at least the largest eigenvalue of M_alpha_delta.
    min_evc = min(np.linalg.eigvals(M.calculateMidpoint()))
    max_evd = max(np.linalg.eigvals(M.calculateRadius()))
    return min_evc >= max_evd

def second_condition(M):
    # Check if M_alpha_c - M_alpha_delta * diag(z) is positive semidefinite for every z.
    Mc = M.calculateMidpoint()
    Md = M.calculateRadius()
    z = np.diag([1] * M.rows)

    M_combined = Mc - np.dot(Md, z)

    # Check if all eigenvalues are non-negative
    return np.all(np.linalg.eigvals(M_combined) >= 0)