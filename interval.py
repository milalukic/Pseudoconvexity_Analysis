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
