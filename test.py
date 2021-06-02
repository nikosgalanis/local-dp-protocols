import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

values = [10,23,43,54,23,19,34,95,23,129,34,2344,23,54,76,123,43,9,345,29,344,208,987,283,123,375,954,542,45,34,65,89,34,75,399,23,54,12,5,346,231,543,2362,46,234,23,48,78,78,34]

real_values = [100 * values[i] / sum(values) for i in range(len(values))]

print(real_values)

arr = np.zeros(len(values))
options = [i for i in range(len(values))]

ages = np.zeros(200000)

for i in range(200000):
	# choose a value given the probabilities for each one
	pert = random.choices(options, real_values)[0]
	arr[pert] += 1
	ages[i] = int(pert)

# print(sum(real_values))

# df = pd.DataFrame(ages).astype(int)

# df.to_csv("new_ages.csv" , index=False)


plt.bar(options, arr)
plt.show()