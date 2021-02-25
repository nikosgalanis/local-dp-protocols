from LDP.RAPOR import *
from LDP.Random_Matrix import *
from LDP.Direct_Encoding import *
from LDP.Unary_Encoding import *
from LDP.Histogram_Encoding import *

import pandas as pd
import numpy as np
import random
import math
import numbers
import copy

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
	
	def __init__(self, domain_size, method = '', epsilon = 1,
				 p = 0.75, q = 0.25, public_matrix = None, m = 10, 
				 f = 0.25, unary_optimized = True, threshold = 0.67, aggr_method = 'THE'):
		# keep the initialization values of the class
		self.domain_size = domain_size
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
			self.protocol_class = RAPOR(f, domain_size, p ,q)
		elif method == 'Radnom_Matrix':
			if public_matrix == None:
				self.public_matrix = generate_matrix(m, domain_size)
			self.protocol_class = Random_Matrix(public_matrix, m, domain_size, epsilon)
		elif method == 'Direct_Encoding':
			self.protocol_class = Direct_Encoding(epsilon, domain_size)
		elif method == 'Histogram_Encoding':
			self.protocol_class = Histogram_Encoding(epsilon, domain_size)
		elif method == 'Unary_Encoding':
			self.protocol_class = Unary_Encoding(epsilon, domain_size, unary_optimized, p, q)
		else:
			raise ValueError('Method not recognized. Choose one of the default ones')
	"""
	Randomization: The user provides a value v in the range (0, d-1), and according to the protocol chosen,
	the system can return either a single value, or a vector containing the randomized values

	The return value of this function makes no sense to someone that views _only_ one user's data. It is used
	by another function, but only to the aggregator of the data
	"""
	def randomize_value(self, v):
		# just call the randomization function of the relevant protocol
		return self.protocol_class.randomize(v)

	"""
	Aggregation: Used by the aggregator in order to combine all the users' data in order to produce the final
	frequency vector, for each value in the domain.

	The reported_values argument is a vector containing each noisy value reported.
	"""
	def aggregate(self, reported_values):
    	# create a dict with all the settings of a protocol, and pass it to the aggregator
		# who chooses the ones that he wants	
		config = {'reported_values': reported_values, 'f': self.f, 'd':self.domain_size,
				  'public_matrix': public_matrix, 'epsilon': self.epsilon, 'threshold':self.threshold,
			      'method': self.aggr_method}
		# call the aggregation function of the relevant protocol
		return self.protocol_class.aggregate(config)


	"""
	Test an previously initialized protol. The function returns the true, and the randomizes
	stats produced in 2 np vectors. Then, the user is free to compare the vectors using the
	neccessary metrics.

	The arguments are: a _csv_ file, with only one column, the one that we are interested in.
	All the other settings for the protocol are already defined, and thus this function is
	able to use them.
	"""
	def test_protocol(self, input_file=None, values=None):
		if input_file is None and values is None:
			raise ValueError('An input file or a value vector must by given')
		if input_file is not None:
			# parse the file, and store its values 
			df = pd.read_csv(input_file)
			values = df.to_numpy()

		# determine the number of users and values, based on the values' vector
		user_count = len(df)
		total_values = len(df)
		# list to store the multiple instances of the user classes
		user_instances = []
		# fill up the list
		for _ in range(user_count):
			user_instances.append(copy.copy(self.protocol_class))
		
		# vector to store the true sums for each value in the domain
		true_results = np.zeros(domain_size)
		
		# list to store the results of each randomization, and to be fed to the aggregator
		reported_values = []

		for user in range(user_count):
			# get the true value
			value = int(values[user])
			# the true sum of this value is increased
			true_results[value] += 1
			# call the randomization function in order to obtain the randomized value
			randomised_result = user_instances[user].randomize(value)
			# and append it to the appropriate list
			reported_values.append(randomised_result)

		# feed the reported values to the aggregator, who returns an np vector with
		# the randomized sums	
		randomised_results = self.aggregate(reported_values)

		# return the tuple of the 2 vectors: the real sums, and the predicted, randomized sums
		return (true_results, randomised_results)


