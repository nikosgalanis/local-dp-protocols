from LDP.RAPOR import *
from LDP.Random_Matrix import *
from LDP.Direct_Encoding import *
from LDP.Unary_Encoding import *
from LDP.Histogram_Encoding import *

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
 - 
"""
class Frequency_Estimator():
	
	def __init__(self, domain_size, method = '', epsilon = 1,
				 p = 0.75, q = 0.25, public_matrix = None, m = 10, 
				 f = 0.25, unary_optimized = True, threshold = 0.67, aggr_method = 'THE'):
		
		self.domain_size = domain_size
		self.method = method
		self.epsilon = epsilon
		self.p = p
		self.q = q
		self.m = m
		self.f = f
		self.threshold = threshold
		self.public_matrix = public_matrix

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

	def randomize_value(self, v):
		return self.protocol_class.randomize(v)

	def aggregate(self, reported_values):
		return self.protocol_class.aggregate(reported_values, f = self.f,
									d = self.domain_size, public_matrix = self.public_matrix, 
									e = self.epsilon, threshold = self.threshold, method = self.aggr_method)