import pseudoconvexity_analysis as pca
import numpy as np
import sympy as sp

from pseudoconvexity_analysis import Interval


sp_symbols = sp.symbols('x')
f = pca.f4(sp_symbols, 0, 1)
f_neg = -f
f_log = sp.log(f)
f_log_neg = -f_log

functions = [f, f_log, f_neg, f_log_neg]
descriptor = ["pseudoconvex", "log-convex", "pseudoconcave", "log-concave"]
symbols = [str(sp_symbols)]

intervals = [
        Interval(-3, 0)
    ]

alpha = [a/100 for a in range(0, 100, 5)]
checkers = [False, False, False, False]
i=0
for function, descriptor in zip(functions, descriptor):
        H = pca.compute_hessian(function, symbols)
        g = pca.compute_gradient(function, symbols)
        for a in alpha:
                M = pca.compute_M(H, g, intervals, symbols, a)
                if pca.first_condition(M) or pca.second_condition(M):
                        print("The function", function , " is", descriptor , "on ", intervals, " for alpha = ", a)
                        checkers[i] = True
                        break
                else:
                        continue
        if not checkers[i]:
                print("The function", f , " is NOT", descriptor,  " on ", intervals)
        i+=1


