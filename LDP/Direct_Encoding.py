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

		false_xs = [i for i in range(self.d) if i != x]		

		pert = random.choice(false_xs)
		
		return pert

	def randomize(self, v):
		return self.perturbe(self.encode(v))
	

	def aggregate(self, reported_values, e, d, *_):
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


		return results

user_count = 50000
domain_size = 10
e = 0.7

users = []

for _ in range(user_count):
    users.append(Direct_Encoding_Client(e, domain_size))

true_results = np.zeros(domain_size)

reported_values = []

for user in range(user_count):
    value = random.randint(0, domain_size - 1)
    true_results[value] += 1

    randomized_result = users[user].randomize(value)
    reported_values.append(randomized_result)

randomized_results = Direct_Encoding_aggregator(reported_values, e, domain_size)

print(true_results)
print(randomized_results.round())