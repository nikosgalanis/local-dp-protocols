import numpy as np
import random
import math
import numbers

class Unary_Encoding():
	def __init__(self, e, d, optimized=True, p=0, q=0):
		self.d = d
		self.p = p
		self.q = q
		self.e = e
		self.optimized = optimized
		
		if self.optimized:
			p = 1 / 2 
			q = 1 / (math.exp(self.e) + 1)
		
	def encode(self, v):
		assert(v < self.d)
		B = np.zeros(self.d)
		B[v] = 1
		return B
	
	def preturb(self, ret):
		B = ret

		new_B = B
		for i in range(len(B)):
			if B[i] == 1:
				pr = self.p
			else: 
				pr = self.q
		
			res = random.random()

			if res < pr:
				new_B[i] = 1
			else:
				new_B[i] = 0
		
		return new_B

	def randomize(self, v):
		return self.perturb(self.encode(v))