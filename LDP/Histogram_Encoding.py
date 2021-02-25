import numpy as np
import random
import math
import numbers

class Histogram_Encoding():
	def __init__(self, e, d):
		self.e = e
		self.d = d

	def encoding(self, v):

		assert(v < self.d)
		B = np.zeros(self.d)
		B[v] = 1
		return B
	
	def perturb(self, ret):
		B = ret
		for i in range(len(B)):
			B[i] = np.random.laplace(scale = (2/self.e))
		
		return B
	
	def randomize(self, v):
		return self.perturbe(self.encode(v))
	
	def aggregate(self, config):

		reported_values = config['reported_values']
		e = config['epsilon']
		d = config['d']
		threshold = config['threshold']
		method = config['method']

		results = np.zeros(d)
		if method == 'SHE':
			for i in range(d):
				sum_v = 0
				for j in reported_values:
					sum_v += j[i]
			
				results[i] = sum_v

			return results
		else:
			# optimal threshold in (1/2, 1)
			results = np.zeros(d)
			n = len(reported_values)

			p = 1 - (1/2) * math.exp((e/2) * (threshold - 1))
			q = (1/2) * math.exp(-(e/2) * threshold)

			for i in range(d):
				sum_v = 0
				for j in reported_values:
					if j[i] > threshold:
						sum_v += j[i]
			
				results[i] = ((sum_v) - n * q) / (p - q)

			return results

