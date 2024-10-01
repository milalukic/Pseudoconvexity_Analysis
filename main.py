import pseudoconvexity_analysis as pca
import tests_unofficial as tests
import sympy as sp
from interval import Interval

sp_symbols = sp.symbols('x')
f = tests.gamma(sp_symbols, 0.5, 1.0)
f_neg = -f
f_log = sp.log(f)
f_log_neg = -f_log

functions = [f, f_log, f_neg, f_log_neg]
descriptor = ["pseudoconvex", "log-convex", "pseudoconcave", "log-concave"]
symbols = ['x']

intervals = [
    Interval(1.0, 1.05)  # Interval for x
#     ,Interval(2.0, 2.99999999999)     # Interval for y (adjust as needed)
]

alpha = [a/100 for a in range(0, 900, 5)]
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


