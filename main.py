import pseudoconvexity_analysis as pca
import numpy as np
import sympy as sp

from pseudoconvexity_analysis import Interval


sp_symbols = sp.symbols('x y')
f = pca.f3(sp_symbols[0], sp_symbols[1])

symbols = [str(symbol) for symbol in sp_symbols]

H = pca.compute_hessian(f, symbols)
g = pca.compute_gradient(f, symbols)

intervals = [
        Interval(-1, 1), Interval(-1, 1)
    ]

alpha = [a/100 for a in range(0, 100, 5)]
for a in alpha:
        M = pca.compute_M(H, g, intervals, symbols, a)

        if pca.first_condition(M) or pca.second_condition(M):
                print("The function", f , " is pseudoconvex on ", intervals, " for alpha = ", a)
                # break

        else:
                print("The function", f , " is NOT pseudoconvex on ", intervals,  " for alpha = ", a)