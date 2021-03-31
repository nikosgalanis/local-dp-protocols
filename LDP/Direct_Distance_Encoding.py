import numpy as np
import random
import math
import numbers

class Direct_Distance_Encoding_client():
	def __init__(self, e, d, threshold):
		# initialization of the protocol's constants
		self.e = e
		self.d = d
		self.theta = threshold
		self.a = (threshold * (threshold + 1)) / (3 * threshold ** 2 - threshold + d - 1)

		# self.p = (math.exp(self.e)) / (d ** 2 + math.exp(self.e) - 1)
		# self.p = math.exp(self.e) / (math.exp(self.e) + (math.sqrt(d) + 1) * (math.sqrt(d) + math.sqrt(d + 1)))
		self.p = self.a
		print("----------------------------", self.p)

	# encoding: simply return the value itself
	def encode(self, v):
		return v

	# perturbation: choose a random value, with fixed probabilities depending on the distance from the truth
	def perturbe(self, ret):
		x = ret
		# increase the value by 1, as we want to avoid division by 0
		x += 1
		# create an array of probabilities for each element of the domain
		probabilities = np.zeros(self.d)

		# fixed alpha constant
		# a = (1 - self.p) / (2 - (1 / x) - (1 / (self.d - x + 1)))
		# a = (1 - self.p) / (math.sqrt(x) + math.sqrt(self.d - x + 1))

		for i in range(self.d):
			# probablitiy of choosing the truth, fixed by the user
			if i == x:
				probabilities[i] = 100 * self.p
			elif abs(i - x) <= self.theta:
    			# probability of lying, depending on the distance of the false value from the true one
				probabilities[i] = 100 * (self.a / ((abs(i - x)) * (abs(i - x) + 1)))
			else:
				probabilities[i] = 100 * self.a / (self.theta * (self.theta + 1))
		# list of all the possible options of values
		options = [i for i in range(self.d)]
		# choose a value given the probabilities for each one
		pert = random.choices(options, probabilities)[0]
		if (x == 21):
			print("sum is ", sum(probabilities))
			print(probabilities)

		return pert

	# randomization consists of perturbing the encoded value
	def randomize(self, v):
		return self.perturbe(self.encode(v))


class Direct_Distance_Encoding_aggregator():
	def __init__(self, e, d, threshold):
    		# initialization of the protocol's constants
		self.e = e
		self.d = d
		self.theta = threshold
		# p and q are fixed, depending on the domain size and the epsilon value
		self.p = math.exp(self.e) / (math.exp(self.e) + self.d - 1)
		self.q = 1 / (math.exp(self.e) + self.d - 1)

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
				if j == i + 1:
					sum_v += 1
			# we do not normalize, we take the results ase given to us by the users
			results[i] = sum_v
			
		return results


