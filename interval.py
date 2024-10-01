class Interval:
    def __init__(self, start, end):
        if start > end:
            raise ValueError("Start of interval cannot be greater than end.")
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f"({self.start}, {self.end})"
    
    def __neg__(self):
        return Interval(-self.end, -self.start)
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Interval(self.start + other, self.end + other)
        return Interval(self.start + other.start, self.end + other.end)

    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Interval(self.start - other, self.end - other)
        return Interval(self.start - other.end, self.end - other.start)
    
    def __mul__(self, other):
        lower = min(self.start * other.start, self.start * other.end,
                     self.end * other.start, self.end * other.end)
        upper = max(self.start * other.start, self.start * other.end,
                     self.end * other.start, self.end * other.end)
        return Interval(lower, upper)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if other.start <= 0 <= other.end:
            raise ValueError("Division by interval containing zero is undefined.")
        lower = min(self.start / other.start, self.start / other.end,
                     self.end / other.start, self.end / other.end)
        upper = max(self.start / other.start, self.start / other.end,
                     self.end / other.start, self.end / other.end)
        return Interval(lower, upper)
    
    def __rtruediv__(self, other):
        if self.start <= 0 <= self.end:
            raise ValueError("Division by an interval containing zero is undefined.")
        lower = min(other / self.end, other / self.start)
        upper = max(other / self.end, other / self.start)
        return Interval(lower, upper)
    
    def __pow__(self, exp):

        if self.start == self.end:
            return self.start**exp

        if isinstance(exp, Interval):
            exponent = exp.start
            if exponent != exp.end:
                raise TypeError("Exponent can't be an interval.") 
        else:
            exponent = exp
        if isinstance(exponent, int):
            if exponent == 0:
                return Interval(1, 1)  # Any number to the power of 0 is 1
            if exponent < 0:
                return (1 / Interval(self.end, self.start)) ** -exponent  # Handle negative exponent
            # Handle cases where the interval includes negative numbers and the exponent is even
            if exponent % 2 == 0:
                return Interval(max(self.start, 0) ** exponent, self.end ** exponent)
            result = Interval(self.start, self.end)
            for _ in range(exponent - 1):
                result *= Interval(self.start, self.end)
            return result
        elif isinstance(exponent, float):
            return Interval(max(0, self.start ** exponent), self.end ** exponent)
        else:
            raise TypeError("Exponent must be an int or float.")
        
    def __rpow__(self, base):
        if isinstance(base, (int, float)):
            if base > 0:  # Check if base is positive
                lower_bound = base ** self.start
                upper_bound = base ** self.end
                return Interval(lower_bound, upper_bound)
            else:
                raise ValueError("Base must be positive for real interval exponentiation.")
        else:
            raise TypeError("Base must be a real number.")
    
    def midpoint(self):
        return 0.5 * (self.start + self.end)

    def radius(self):
        return 0.5 * (self.end - self.start)
