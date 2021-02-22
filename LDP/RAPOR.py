import numpy as np
import random

class RAPOR():
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
			# if it does not exsist, we must create it
			new_B = np.zeros(self.d)
			# for each item, we must fix it according to its value in the original matrix
			for i, b in enumerate(new_B):
				# if the element is 1
				if B[i] == 1:
					pr = 1 - 0.5 * self.f
				# if it is 0
				else:
					pr = 0.5 * f
				# generate a random number
				res = random.random()
				# and compute the element in the new matrix
				if (res < pr):
					new_B[i] = 1
				else:
					new_B[i] = 0
			# save it to the dictionary so we do not have to compute it again
			self.perma_B[v] = new_B

		# __step 2__: instantaneuos randomized response       
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

	def aggregate(self, reported_values, f, d, *_):
		results = np.zeros(d)
		for i in range(d):
			sum_v = 0
			for j in reported_Bs:
				sum_v += j[i]

			results[i] = (sum_v - 0.5 * f * len(reported_Bs)) / (1 - f)
		
		return results


user_count = 30000
domain_size = 30
total_values = 50000

f = 0.5
p = 0.75
q = 0.25

users = []
for _ in range(user_count):
	users.append(RAPOR_client(f, domain_size, p, q))

true_results = np.zeros(domain_size)

reported_Bs = []
for user in range(user_count):
	value = random.randint(0, domain_size - 1)
	true_results[value] += 1

	randomised_result = users[user].randomize(value)
	reported_Bs.append(randomised_result)


randomised_results = RAPPOR_aggregator(reported_Bs, f, domain_size)

print(true_results)
print(randomised_results)