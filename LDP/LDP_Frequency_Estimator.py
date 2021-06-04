from RAPPOR import *
from Random_Matrix import *
from Direct_Encoding import *
from Distance_Sensitive_Encoding import *
from Unary_Encoding import *
from Histogram_Encoding import *

import pandas as pd
import numpy as np
import random
import math
import numbers
import copy
import tqdm as tq
import qif
# Base class for the frequency estimator
"""
Mandatory Arguments:

 - domain_size: the number of values that the user might answer to the question posed
 - method: the protocol that the user wants to use. Possible answers:
 		-> 'RAPPOR'
		-> 'Random_Matrix'
		-> 'Direct_Encoding'
		-> 'Histogram_Encoding'
		-> 'Unary_Encoding'

Optional Arguments (depending on the protocol used):

 - epsilon: The epsilon value, as a setting for LDP (Usually in the range (0, 5]))
 - p, q: Probability values used by pure protocols. In some cases the do not need to be included
 - Public matrix: The matrix that was previously generated in the Random Matrix protocol
 - m: The m value used for the initialization of the public matrix in the R.M. protocol
 - f: The frequency setting used by the RAPPOR protocol
 - unary_optimized: setting for optimizing the Unary Encoding protocol; by default set to True
 - threshold: threshold used for the aggregation during the histogram encoding
 - aggregation_method: aggr. method used my the histogram encoding, in order to obtain the randomized values. ('SHE' or 'THE')
"""
class Frequency_Estimator():
	
	def __init__(self, domain_size, method = 'Direct_Encoding', epsilon = 1,
				 p = 0.75, q = 0.25, public_matrix = None, m = 10, n_users = 1,
				 f = 0.25, unary_optimized = True, threshold = 0.67, 
				 aggr_method = 'THE'):
		# keep the initialization values of the class
		self.domain_size = domain_size
		self.n_users = n_users
		self.method = method
		self.epsilon = epsilon
		self.p = p
		self.q = q
		self.m = m
		self.f = f
		self.threshold = threshold
		self.public_matrix = public_matrix
		# according to the method, initialize the proper class with the mandatory arguments
		if method == 'RAPPOR':
			self.user_protocol_class = RAPPOR_client(f, domain_size, p ,q)
			self.aggregator_protocol_class = RAPPOR_aggregator(f, domain_size, p ,q)
		elif method == 'Random_Matrix':
    		# spectial case: if we are using random matrix we must provide a public matrix
			# if it is not provided, create it on the fly using the appropriate function
			if public_matrix == None:
				self.public_matrix = generate_matrix(m, domain_size)
			self.user_protocol_class = Random_Matrix_client(self.public_matrix, m, domain_size, epsilon)
			self.aggregator_protocol_class = Random_Matrix_aggregator(public_matrix, m, domain_size, epsilon)
		elif method == 'Direct_Encoding':
			self.user_protocol_class = Direct_Encoding_client(epsilon, domain_size)
			self.aggregator_protocol_class = Direct_Encoding_aggregator(epsilon, domain_size)
		elif method == 'Distance_Sensitive_Encoding':
			self.user_protocol_class = Distance_Sensitive_Encoding_client(epsilon, domain_size)
			self.aggregator_protocol_class = Distance_Sensitive_Encoding_aggregator(epsilon, domain_size)
		
		elif method == 'Histogram_Encoding':
			self.user_protocol_class = Histogram_Encoding_client(epsilon, domain_size)
			self.aggregator_protocol_class = Histogram_Encoding_aggregator(epsilon, domain_size)
		elif method == 'Unary_Encoding':
			self.user_protocol_class = Unary_Encoding_client(epsilon, domain_size, unary_optimized, p, q)
			self.aggregator_protocol_class = Unary_Encoding_aggregator(epsilon, domain_size, unary_optimized, p, q)
		else:
			raise ValueError('Method not recognized. Choose one of the default ones')
		
		# create a list containing one instance for each user
		self.users = []
		for _ in range(self.n_users):
			self.users.append(copy.copy(self.user_protocol_class))
	
	
	"""
	Randomization: The user provides a value v in the range (0, d-1), and according to the protocol chosen,
	the system can return either a single value, or a vector containing the randomized values

	The return value of this function makes no sense to someone that views _only_ one user's data. It is used
	by another function, but only to the aggregator of the data
	"""
	def randomize_value(self, v):
		# just call the randomization function of the relevant protocol
		return self.user_protocol_class.randomize(v)

	
	
	"""
	Aggregation: Used by the aggregator in order to combine all the users' data in order to produce the final
	frequency vector, for each value in the domain.

	The reported_values argument is a vector containing each noisy value reported.
	"""
	def aggregate(self, reported_values):
    	# create a dict with all the settings of a protocol, and pass it to the aggregator
		# who chooses the ones that he wants	
		config = {'reported_values': reported_values, 'f': self.f, 'd':self.domain_size,
				  'public_matrix': self.public_matrix, 'epsilon': self.epsilon, 'threshold':self.threshold,
			      'method': self.method, 'p': self.p, 'q': self.q}
		# call the aggregation function of the relevant protocol
		return self.aggregator_protocol_class.aggregate(config)


	
	"""
	Test an previously initialized protol. The function returns the true, and the randomizes
	stats produced in 2 np vectors. Then, the user is free to compare the vectors using the
	neccessary metrics.

	The arguments are: a _csv_ file, with only one column, the one that we are interested in.
	All the other settings for the protocol are already defined, and thus this function is
	able to use them.
	"""
	def test_protocol(self, count, input_file=None, values=None):
		if input_file is None and values is None:
			raise ValueError('An input file or a value vector must by given')
		if input_file is not None:
			# parse the file, and store its values 
			df = pd.read_csv(input_file)
			values = df.to_numpy()

		# determine the number of users and values, based on the values' vector
		user_count = max(df.iloc[:,0]) + 1
		total_values = len(df.iloc[:,1]) + 1

		df = df[:count]
		# check that the users are the same with the way that we initialized the class
		if user_count != self.n_users:
    			raise ValueError('Incorrect amount of users during initialization')

		# vector to store the true sums for each value in the domain
		true_results = np.zeros(self.domain_size)
		
		# list to store the results of each randomization, and to be fed to the aggregator
		reported_values = []

		# for i in tq.tqdm(range(len(df)), position=0, leave=True):
		for i in range(len(df)):
			# get the true value
			user = int(df.iloc[i, 0])
			value = int(df.iloc[i, 1])

			# value = int(values[user])
			# the true sum of this value is increased
			true_results[value] += 1
			# call the randomization function in order to obtain the randomized value
			randomised_result = self.users[user].randomize(value)
			# and append it to the appropriate list
			reported_values.append(randomised_result)

		# feed the reported values to the aggregator, who returns an np vector with
		# the randomized sums	
		randomised_results = self.aggregate(reported_values)

		# return the tuple of the 2 vectors: the real sums, and the predicted, randomized sums
		return (true_results.astype(int), randomised_results.astype(int))


import matplotlib.pyplot as plt

e = np.log(6)

res = input("Method: [i]: instance | [r]: full run\n\n")

if (res == 'i'):
	estimator = Frequency_Estimator(50, method='Direct_Encoding', epsilon=e, n_users=1000)

	res = estimator.test_protocol(10000, input_file='../res.csv')

	print(res[0])
	print(res[1])

	print("\nsums\n\n", np.sum(res[0]), np.sum(res[1]), "\n\n")

	estimator = Frequency_Estimator(50, method='Distance_Sensitive_Encoding', epsilon=e, n_users=1000)

	res1 = estimator.test_protocol(10000, input_file='../res.csv')

	print(res1[0])
	print(res1[1])

	print("\nsums\n\n", np.sum(res1[0]), np.sum(res1[1]), "\n\n")

	xs = [i for i in range(50)]
	fig, axs = plt.subplots(3)
	fig.suptitle('Vertically stacked subplots')
	axs[0].bar(xs, res[0])
	axs[1].bar(xs, res[1])
	axs[2].bar(xs, res1[1])

	# axs[0].set_ylim((0, 20))
	axs[1].set_ylim((0, max(res[0])))
	axs[2].set_ylim((0, max(res[0])))

	axs[0].title.set_text('True Data')
	axs[1].title.set_text('Perturbed Data produced by the Direct Encoding Protocol')
	axs[2].title.set_text('Perturbed Data produced by our Protocol')

	def euclid(x, y):                       # ground distance
		return abs(x-y)

	kant = qif.metric.kantorovich(euclid)   # distance on distributions


	print("\n\n\n\nDirect:", kant(res[0], res[1]))
	print("\n\n\n\nDistance_Sensitive:", kant(res1[0], res1[1]))

	plt.show()

else:

	direct = []
	dist_direct = []
	dist_hist = []

	max_samples = 1000

	x = [i for i in range(10, max_samples, 10)]

	e = np.log(12)
	d = 50

	def euclid(x, y):                       # ground distance
		return abs(x-y)

	kant = qif.metric.kantorovich(euclid)   # distance on distributions


	# for i in range(10, 10000, 10):
	for i in tq.tqdm(range(10, max_samples, 10), position=0, leave=True):

		estimator = Frequency_Estimator(50, method='Direct_Encoding', epsilon=e, n_users=1000)
		reses = []
		for j in range(0, 10):
			a = estimator.test_protocol(i, input_file='../res.csv')
			reses.append(kant(a[0], a[1]))
		res = sum(reses) / len(reses) 

		direct.append(res / i)

		estimator = Frequency_Estimator(50, method='Distance_Sensitive_Encoding', epsilon=e, n_users=1000)

		reses = []
		for j in range(0, 10):
			a = estimator.test_protocol(i, input_file='../res.csv')
			reses.append(kant(a[0], a[1]))

		res1 = sum(reses) / len(reses)

		dist_direct.append(res1 / i)

		estimator = Frequency_Estimator(50, method='Histogram_Encoding', epsilon=e, n_users=1000)

		reses = []
		for j in range(0, 10):
			a = estimator.test_protocol(i, input_file='../res.csv')
			reses.append(kant(a[0], a[1]))

		res2 = sum(reses) / len(reses)

		dist_hist.append(res2 / i)

	plt.plot(x, direct, 'r')
	plt.plot(x, dist_hist, 'g')
	plt.plot(x, dist_direct, 'b')


	plt.legend(["Direct Encoding", "Histogram Encoding", "Distance Sensitive Encoding"])
	plt.savefig('../misc/latest_plot.png')
	plt.show()