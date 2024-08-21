import pseudoconvexity_analysis as pca
import numpy as np
import sympy as sp

from pseudoconvexity_analysis import IntervalMatrix, Interval


symbols = sp.symbols('x y')
f = pca.f2(symbols[0], symbols[1])

H = pca.compute_hessian(f, symbols)
g = pca.compute_gradient(f, symbols)

i = -5
j = 5

numits = 0

while i<=j and numits < 11:

    p = np.random.randint(0,10)
    if(p<5):
        i+=0.5
    else:
        j-=0.5
    intervals = [
        Interval(i, j), Interval(i, j)
    ]

    M = pca.compute_M(H, g, intervals)
    print(intervals)
    print(M.intervals[0])

    if pca.first_condition(M) or pca.second_condition(M):
        print("The function is pseudoconvex on ", intervals)
    else:
        print("The function is NOT pseudoconvex on ", intervals)

    numits+=1    