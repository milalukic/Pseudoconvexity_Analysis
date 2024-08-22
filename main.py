import pseudoconvexity_analysis as pca
import numpy as np
import sympy as sp

from pseudoconvexity_analysis import Interval


sp_symbols = sp.symbols('x y')
f = pca.f2(sp_symbols[0], sp_symbols[1])

symbols = [str(symbol) for symbol in sp_symbols]

H = pca.compute_hessian(f, symbols)
g = pca.compute_gradient(f, symbols)

intervals = [
        Interval(-1, 2), Interval(-1, 2)
    ]

M = pca.compute_M(H, g, intervals, symbols)

if pca.first_condition(M) or pca.second_condition(M):
        print("The function is pseudoconvex on ", intervals)
else:
        print("The function is NOT pseudoconvex on ", intervals)