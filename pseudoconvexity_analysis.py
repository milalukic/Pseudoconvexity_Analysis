# import tangent
import numpy as np
import sympy as sp

from interval_matrix import IntervalMatrix, Interval
from tests_unofficial import f_der1, f_der2, f2_der1, f2_der2

# Computing the hessian matrix and gradients from a function 
def compute_hessian(f, symbols):
    # pass
    hessian_matrix = sp.hessian(f, symbols)
    return hessian_matrix

def compute_gradient(f, symbols):
    gradient = []
    for symbol in symbols:
        gradient.append(sp.diff(f, symbol))
    return np.array(gradient)

def compute_M(H, g, intervals, alpha=1.0):

    # M_alpha = H + alpha*g*g^T - actual formula to calculate M
    gt = g.reshape(-1,1)
    M = H + alpha* np.outer(g, gt)

    # TODO: make this expression evaluation automatic. It took too long for me to figure out so I just did it like this temporarily
    # Calculated the expressions from M by hand 
    interval_value1 = f2_der1(intervals[0], intervals[1])
    interval_value2 = f2_der2(intervals[0], intervals[1])
    interval_value3 = f2_der1(intervals[1], intervals[0])

    intervals_evaluated = [[interval_value1, interval_value2], 
                           [interval_value2, interval_value3]]

    # TODO: automatically make this with a bunch of ugly loops   
    # 3d 
    # x2 xy xz 
    # xy y2 yz
    # xz yz z2

    # create a matrix
    IM = IntervalMatrix(intervals_evaluated)
    # return the matrix M_alpha
    return IM

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
    
    M_combined = Mc - Md*z

    # positive semidefinite = all eigvals >= 0
    return np.all(np.linalg.eigvals(M_combined) >= 0)
