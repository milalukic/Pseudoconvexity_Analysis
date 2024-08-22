from interval import Interval
import numpy as np
import math

class IntervalMatrix:
    def __init__(self, intervals):
        self.rows = int(math.sqrt(len(intervals)))
        self.cols = self.rows
        
        self.intervals = []

        it = 0

        for _ in range(self.rows):
            self.intervals.append(intervals[it:self.cols+it])
            it+=self.cols
    
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
        midpoint_matrix = np.zeros((self.rows, self.rows))
        for i in range(self.rows):
            for j in range(self.cols):
                midpoint_matrix[i][j] = self.intervals[i][j].midpoint()

        return midpoint_matrix

    def calculateRadius(self):
        radius_matrix = np.zeros((self.rows, self.rows))
        for i in range(self.rows):
            for j in range(self.cols):
                radius_matrix[i][j] = self.intervals[i][j].radius()

        return radius_matrix
