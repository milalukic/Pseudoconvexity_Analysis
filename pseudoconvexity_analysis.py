import tangent
import numpy as np
import sympy as sp

# Function 1 EXAMPLE f(x, y) = x^2 + y^2 - Will be generalized later
def f(x, y):
    return x**2 + y**2
# Won't work like this but i want to move on - temporary solutions
def f_der1(x, y):
    return (x**2)*4.0 + 2
def f_der2(x, y):
    return x*4.0 * y

# Function 2 EXAMPLE f(x, y) = ln(1 + x^2 + y^2)
def f2(x, y):
    return  x**2 + x*y + y**2
def f2_der1(x, y):
    return 2
def f2_der2(x, y):
    return 1

def diff1(f):
    return tangent.grad(f)

class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f"[{self.start}, {self.end}]"
    
    # Defining interval addition logic.
    def __add__(self, other):
        if isinstance(other, (int, float)):
            # Addition with a constant
            return Interval(self.start + other, self.end + other)
        return Interval(self.start + other.start, self.end + other.end)  

    # Defining interval substraction logic.
    def __sub__(self, other):
        return Interval(self.start - other.end, self.end - other.start)  
    
    # Defining interval multiplication logic.
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            # Multiplication with a constant
            return Interval(self.start * other, self.end * other)
        else:
            M = [self.start*other.start, self.start*other.end, self.end*other.start, self.end*other.end];
            return Interval(min(M), max(M))
    
    # Defining interval division logic.
    def __truediv__(self, other):
        if other.start <= 0 <= other.end:
            return ValueError("You can't divide with an interval including 0")
        
        divisions = Interval(1.0/other.end, 1.0/other.start)

        return self*divisions

    def __pow__(self, exponent):
        result = Interval(self.start, self.end)
        for i in range(exponent-1):
            result *= Interval(self.start, self.end)

        return result

class IntervalMatrix:
    def __init__(self, intervals):
        self.intervals = intervals
        self.rows = len(self.intervals)
        self.cols = 2
    
    def __str__(self) -> str:
        # each row in a
        return "\n".join([str(row) for row in self.intervals])
    
    def get_interval(self, i, j) -> Interval:
        return self.intervals[i][j]
    
    def set_interval(self, i, j, interval):
        self.intervals[i][j] = interval
    
    # Adds two interval matrices.
    def add(self, other):
        if self.rows != other.rows and self.cols != other.cols:
            return ValueError("Matrices must have the same shape for addition")

        result_intervals = []
        for i in range(self.rows):
            for j in range(self.cols):
                result_intervals[i][j] = self.get_interval(i, j) + other.get_interval(i, j)
        return IntervalMatrix(result_intervals)
    
    def multiply(self, other):
        rows_A = self.rows
        cols_A = self.cols
        rows_B = other.rows
        cols_B = other.cols

        if cols_A != rows_B:
            return ValueError("Number of columns in first matrix must equal number of rows in second matrix")
        
        result_intervals = []
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result_intervals[i][j] += self.intervals[i][k]*other.intervals[k][j]
        
        return IntervalMatrix(result_intervals)
    
    def calculateMidpoint(self):
        midpoint_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                midpoint_matrix[i][j] += 0.5 * (self.intervals[i][j] + self.intervals[i][j])

        return np.array(midpoint_matrix)

    def calculateRadius(self):
        radius_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                radius_matrix[i][j] += 0.5 * (self.intervals[i][j] - self.intervals[i][j])

        return radius_matrix

# Computing the hessian matrix and gradients from a function 
def compute_hessian(f, symbols):
    pass
    # hessian_matrix = sp.hessian(f, symbols)
    # return hessian_matrix

def compute_gradient(f):
    pass
    gradient = []
    # for symbol in symbols:
    #     gradient.append(sp.diff(f, symbol))
    # return np.array(gradient)

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

# def __main__():
symbols = sp.symbols('x y')
f = f2(symbols[0], symbols[1])

H = compute_hessian(f, symbols)
g = compute_gradient(f, symbols)

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

    M = compute_M(H, g, intervals)
    print(intervals)
    print(M.intervals[0])

    if first_condition(M) or second_condition(M):
        print("The function is pseudoconvex on ", intervals)
    else:
        print("The function is NOT pseudoconvex on ", intervals)

    numits+=1    