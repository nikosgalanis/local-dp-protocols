import numpy as np
import random
import math
import numbers

def generate_matrix(m, d):
    F = np.zeros((m,d))

    bound = -1 / math.sqrt(m)
    print (bound)
    for i in range(m):
        for j in range(d):
            F[i][j] = bound * random.random()
    print (F)

generate_matrix(5, 10)

class Random_Matrix_Client():
    def __init__(self, F, m, d, e):
        self.F = F
        self.m = m
        self.d = d
        self.e = e
    
    def encode(self, v):
        r = random.randint(0, self.m)
        x = self.F[r][v]

        return (r, x)

    def preturb(self, res):
        r, x = res

        pr = e ** 
