import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def randomized_response(true_value):
	res1 = random.randint(0,1)
	if (res1 == 1):
		return true_value
	else:
		res2 = random.randint(0,1)
		if (res2 == 1):
			return 0
		else:
			return 1


n_users = 30

users = [i for i in range(100, 10000, 100)]
diffs = []
print(users)

for n_users in users:
    
	diff = 0
	for _ in range(100):

		true_values = np.array([random.randint(0,1) for i in range(n_users)])


		new_values = np.array([randomized_response(i) for i in true_values])


		diff += abs(sum(new_values) - sum(true_values))

	diff /= 10
	diffs.append(diff / n_users)

plt.plot(users, diffs)
plt.xlabel("Number of Users")
plt.ylabel("Accuracy Error")
plt.show()