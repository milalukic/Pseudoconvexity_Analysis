from interval import Interval
import numpy as np
import math

class IntervalMatrix:
    def __init__(self, intervals):
        size = int(math.sqrt(len(intervals)))
        self.rows = size
        self.cols = size
        self.intervals = []

        for i in range(size):
            self.intervals.append(intervals[i*size:(i+1)*size])
    
    def __str__(self) -> str:
        return "\n".join([str(row) for row in self.intervals])
    
    def get_interval(self, i, j) -> Interval:
        return self.intervals[i][j]
    
    def set_interval(self, i, j, interval):
        self.intervals[i][j] = interval
    
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
