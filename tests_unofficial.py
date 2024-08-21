# Function 1 EXAMPLE f(x, y) = x^2 + y^2 - Will be generalized later
def f1(x, y):
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
