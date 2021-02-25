import numpy as np
import random
import math
import numbers

class Direct_Encoding():
	def __init__(self, e, d):
		self.e = e
		self.d = d
		self.p = math.exp(self.e) / (math.exp(self.e) + self.d - 1)
		self.q = 1 / (math.exp(self.e) + self.d - 1)

	def encode(self, v):
		return v

	def perturbe(self, ret):
		x = ret

		res = random.random()
		
		if (res < self.p):
			pert = x
		else:
			false_xs = [i for i in range(self.d) if i != x]		

			pert = random.choice(false_xs)
		
		return pert

	def randomize(self, v):
		return self.perturbe(self.encode(v))
	

	def aggregate(self, config):

		reported_values = config['reported_values']
		e = config['epsilon']
		d = config['d']

		results = np.zeros(d)
		n = len(reported_values)
		

		p = math.exp(e) / (math.exp(e) + d - 1)
		q = 1 / (math.exp(e) + d - 1)

		for i in range(d):
			sum_v = 0
			for j in reported_values:
				if j == i:
					sum_v += 1
			
			results[i] = ((sum_v) - n * q) / (p - q)
			if (results[i] < 0):
				results[i] = 0

		return results

import pandas as pd

df = pd.read_csv('../age.csv')

ages = df.to_numpy()


user_count = len(df)
domain_size = 130
total_values = len(df)

# for i in range(len(ages)):
# 	if ages[i] <  60:
# 		ages[i] = 0
# 	else:
# 		ages[i] = 1

e = 1.89

users = []

for _ in range(user_count):
	users.append(Direct_Encoding(e, domain_size))
    
true_results = np.zeros(domain_size)

reported_values = []

for user in range(user_count):
	value = int(ages[user])
	true_results[value] += 1

	randomized_result = users[user].randomize(value)
	reported_values.append(randomized_result)
    		
config = {'reported_values': reported_values, 'd':domain_size,
			'epsilon': e}

randomised_results = users[1].aggregate(config)

print(true_results.astype(int))
print(randomised_results.astype(int))


def test_protocol()