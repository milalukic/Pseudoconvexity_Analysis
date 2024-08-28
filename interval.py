import math
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
        if isinstance(other, (int, float)):
            return Interval(self.start * other, self.end * other)
        else:
            M = [self.start*other.start, self.start*other.end, self.end*other.start, self.end*other.end]
            return Interval(min(M), max(M))
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self/Interval(other, other)
        if other.start <= 0 <= other.end:
            return ValueError("You can't divide with an interval including 0")
        divisions = Interval(1.0/other.end, 1.0/other.start)
        return self*divisions

    def __pow__(self, exponent):
        result = Interval(self.start, self.end)
        if isinstance(exponent, int):
            # Handle cases where the interval includes negative numbers and the exponent is even
            if exponent%2 == 0:
                result.start = max(result.start, 0)
        elif isinstance(exponent, float):
            return Interval(max(0, result.start ** exponent), result.end ** exponent)
        for i in range(exponent-1):
            result *= Interval(self.start, self.end)
        return result
    
    def __rpow__(self, base):
        if isinstance(base, (int, float)):  # Base is a number, interval is the exponent
            if base > 0:  # Check if base is positive
                lower_bound = base**self.start
                upper_bound = base**self.end
                return Interval(lower_bound, upper_bound)
            else:
                raise ValueError("Base must be positive for real interval exponentiation.")
        else:
            raise TypeError("Base must be a real number.")
    
    def midpoint(self):
        return 0.5*(self.start + self.end)

    def radius(self):
        return 0.5*(self.end - self.start)


interval = Interval(1,2)
print(math.e**interval)