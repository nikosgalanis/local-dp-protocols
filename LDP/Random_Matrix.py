import numpy as np
import random
import math
import numbers

def generate_matrix(m, d):
	F = np.zeros((m,d))
	
	bound = -1 / math.sqrt(m)
	for i in range(m):
		for j in range(d):
			F[i][j] = random.uniform(-bound, bound)

	return F
generate_matrix(5, 10)

class Random_Matrix_client():
	def __init__(self, F, m, d, e):
		# initialization of the protocol's constants
		self.F = F
		self.m = m
		self.d = d
		self.e = e
	
	def encode(self, v):
		r = random.randint(0, self.m - 1)
		x = self.F[r][v]

		return (r, x)

	def perturbe(self, ret):
		r, x = ret

		pr = math.exp(self.e) / (math.exp(self.e) + 1)
		res = random.random()
		if (res < pr):
			b = 1
		else:
			b = -1
		
		c = (math.exp(self.e) + 1) / (math.exp(self.e) - 1)

		return (r, b * c * self.m * x)

	def randomize(self, v):
		return self.perturbe(self.encode(v))



class Random_Matrix_aggregator():
	def __init__(self, F, m, d, e):
		# initialization of the protocol's constants
		self.F = F
		self.m = m
		self.d = d
		self.e = e

	def aggregate(self, config):
		
		reported_values = config['reported_values']
		public_matrix = config['public_matrix']
		d = self.d

		results = np.zeros(d)
		for i in range(d):
			sum_v = 0
			for j in reported_values:
				sum_v += j[1] * public_matrix[j[0]][i]
			
			results[i] = sum_v
		return results
