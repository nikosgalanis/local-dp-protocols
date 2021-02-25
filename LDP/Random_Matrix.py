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

class Random_Matrix():
	def __init__(self, F, m, d, e):
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
		return self.perturb(self.encode(v))

	def aggregate(self, config):
		
		reported_values = config['reported_values']
		public_matrix = config['public_matrix']
		d = config['d']

		results = np.zeros(d)
		for i in range(d):
			sum_v = 0
			for j in reported_values:
				sum_v += j[1] * public_matrix[j[0]][i]
			
			results[i] = sum_v
		return results


# user_count = 50000
# domain_size = 10
# m = 100
# e = 0.7

# public_matrix = generate_matrix(m , domain_size)

# users = []

# for _ in range(user_count):
# 	users.append(Random_Matrix_Client(public_matrix, m, domain_size, e))

# true_results = np.zeros(domain_size)

# reported_values = []

# for user in range(user_count):
# 	value = random.randint(0, domain_size - 1)
# 	true_results[value] += 1

# 	randomized_result = users[user].randomize(value)
# 	reported_values.append(randomized_result)

# randomized_results = Random_Matrix_aggregator(reported_values, public_matrix, domain_size)

# print(true_results)
# print(randomized_results.round())