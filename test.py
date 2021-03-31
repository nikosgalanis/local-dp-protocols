import random
import numpy as np

numbers = [1,2,3,4,5,6]

weights = np.zeros(6)
weights[0] = 10
weights[1] = 20
weights[2] = 30
weights[3] = 20
weights[4] = 10
weights[5] = 10



res = np.zeros(6)

for i in range(10000):
    x = random.choices(numbers, weights)[0]
    res[x - 1] += 1

res /= 100

print(sum(res))
print(res)
