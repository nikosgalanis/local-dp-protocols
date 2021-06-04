import numpy as np
import random

class RAPPOR_client():
	# initialize the class with the necessary arguments: f and d(domain size)
	def __init__(self, f, d, p, q):
		self.f = f
		self.d = d
		self.p = p
		self.q = q
	
		# store matrices of permanent perturbation
		self.perma_B = {}
		
	# encode by creating a d-lengthed vector
	def encode(self, v):
		B = np.zeros(self.d)
		# only it's v-th element is 1
		B[v] = 1

		return v, B

	# perturbe the value in order to report it
	def perturb(self, res):
		v, B = res
		# __step 1__: permanent randomized response
		# check if the permanent B exists for the value B
		if v in self.perma_B:
			new_B = self.perma_B[v]
		else:
			# if it does not exist, we must create it
			new_B = np.zeros(self.d)
			# for each item, we must fix it according to its value in the original matrix
			for i, b in enumerate(new_B):
				# if the element is 1
				if B[i] == 1:
					pr = 1 - 0.5 * self.f
				# if it is 0
				else:
					pr = 0.5 * self.f
				# generate a random number
				res = random.random()
				# and compute the element in the new matrix
				if (res < pr):
					new_B[i] = 1
				else:
					new_B[i] = 0
			# save it to the dictionary so we do not have to compute it again
			self.perma_B[v] = new_B

		# __step 2__: instantaneous randomized response       
		final_B = np.zeros(self.d)
		for i, b in enumerate(final_B):
			if new_B[i] == 1:
				pr = self.p
			else:
				pr = self.q
			res = random.random()
			if (res < pr):
				final_B[i] = 1
			else:
				final_B[i] = 0

		return final_B

	# randomization contists of the PE() opperation
	def randomize(self, v):
		return self.perturb(self.encode(v))



class RAPPOR_aggregator():
    	# initialize the class with the necessary arguments: f and d(domain size)
	def __init__(self, f, d, p, q):
		self.f = f
		self.d = d
		self.p = p
		self.q = q
		
	def aggregate(self, config):
    
		reported_values = config['reported_values']	
		f = self.f	
		d = self.d
		n = len(reported_values)
		results = np.zeros(d)
		for i in range(d):
			sum_v = 0
			for j in reported_values:
				if j[i] == 1:
					sum_v += j[i]

			results[i] = (sum_v - 0.5 * f * n) / (1 - f)
		
		return results
	
	def compute_metrics(self, true, randomized):
		metrics_dict = {}
		metrics_dict['eucledian_distance'] = np.linalg.norm(true - randomized)
    