import numpy as np
import random
import math
import numbers

class Distance_Sensitive_Encoding_client():
	def __init__(self, e, d):
		# initialization of the protocol's constants
		self.e = e
		self.d = d
		self.theta = math.floor((math.sqrt(4 * math.exp(self.e) + 1) - 1) / 2)
		self.a = (self.theta * (self.theta + 1)) / (3 * self.theta ** 2 - self.theta + d - 1)
		
		self.p = self.a
		self.probs = [a / i for i in range(1, self.theta)]
		self.q = self.a / (self.theta * (self.theta + 1))

	# encoding: simply return the value itself
	def encode(self, v):
		return v

	# perturbation: choose a random value, with fixed probabilities depending on the distance from the truth
	def perturbe(self, ret):
		x = ret
		# create an array of probabilities for each element of the domain
		probabilities = np.zeros(self.d)
		# extreme cases: x-theta outside domain boundaries
		if (x - self.theta < 0):
			m = sum([self.a / (abs(i - x) * (abs(i - x) + 1)) - self.a / (self.theta * (self.theta + 1)) for i in range(x - self.theta, 0)])
		elif (x + self.theta > self.d):
			m = sum([self.a / (abs(i - x) * (abs(i - x) + 1)) - self.a / (self.theta * (self.theta + 1)) for i in range(d, x + self.theta)])
		else:
			m = 0

		for i in range(self.d):
			# probablitiy of choosing the truth, fixed by the user
			if i == x:
				probabilities[i] = 100 * self.p
			# probability of being within the area
			elif abs(i - x) < self.theta:
    			# probability of lying, depending on the distance of the false value from the true one
				probabilities[i] = 100 * self.probs[abs(i - x) - 1] + m / (self.d - 1)
			# probability of being outside the area
			else:
				probabilities[i] = 100 * self.q + m / (self.d - 1)
		# list of all the possible options of values
		options = [i for i in range(self.d)]
		# choose a value given the probabilities for each one
		pert = random.choices(options, probabilities)[0]
		print(sum(probabilities))
		return pert

	# randomization consists of perturbing the encoded value
	def randomize(self, v):
		return self.perturbe(self.encode(v))


class Distance_Sensitive_Encoding_aggregator():
	def __init__(self, e, d):
    		# initialization of the protocol's constants
		self.e = e
		self.d = d

	def aggregate(self, config):
		# define the needed variables from the configuration dict provided
		reported_values = config['reported_values']
		d = config['d']

		# array to store the results
		results = np.zeros(d)

		# compute the estimation for each value of the domain
		for i in range(d):
			sum_v = 0
			# for each reported value
			for j in reported_values:
    			# report the previous one, because of the (+1) that happened in perturnation
				if j == i:
					sum_v += 1
			# we do not normalize, we take the results ase given to us by the users
			results[i] = sum_v
			
		return results

