import math
import interval
# Function 1 EXAMPLE f(x, y) = x^2 + y^2 - Will be generalized later
def f1(x, y):
    return x**2 + y**2

# Function 2 EXAMPLE f(x, y) = ln(1 + x^2 + y^2)
def f2(x, y):
    return  x**2 + x*y + y**2

# function 3:
def f3(x, y):
    return y - x**2
    
def f4(x, mean, std_dev):
    coefficient = 1 / (std_dev * math.sqrt(2 * math.pi))
    power = -((x - mean) ** 2) / (2 * std_dev ** 2)
    exponent = math.e**power
    return coefficient * exponent