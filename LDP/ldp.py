# %%
import numpy as np
import matplotlib.pyplot as plt
import qif

eps = np.log(20)
d = 89               # domain size
trv = 3              # true value
theta_f = (np.sqrt( 4 * np.exp(eps) + 1) - 1) / 2
theta = int(np.floor( theta_f ))
a = theta * (theta + 1) / (3 * theta**2 - theta + d - 1)
print()


print("range ", [i for i in range(d + 1, trv + theta)])
m = sum([a / (abs(i - trv) * (abs(i - trv) + 1)) - a / (theta * (theta + 1)) for i in range(trv - theta + 1, 0)])
print([a / min(theta, abs(i - trv)) for i in range(-10, 10) if i != trv])
print("m is ", m)


def prob(i, x):
	if i == x:
		return a
	if (x - theta < 0):
		m = sum([a / (abs(i - x) * (abs(i - x) + 1)) - a / (theta * (theta + 1)) for i in range(trv - theta + 1, 0)])
		c = min( abs(i - x), theta)

		return a / ( c * (c+1)) + m / (d - 1)
	
	if (x + theta > (d - 1)):
		m = sum([a / (abs(i - x) * (abs(i - x) + 1)) - a / (theta * (theta + 1)) for i in range(d, x + theta)])
		c = min( abs(i - x), theta)
		
		return a / ( c * (c+1)) + m / (d - 1)

	c = min( abs(i - x), theta)
	return a / ( c * (c+1))

def rr(i, x):
	t = 1 / (d - 1 + np.exp(eps))
	if i == x:
		return np.exp(eps) * t
	else:
		return t


area = sum([prob(trv - j, trv) for j in range(-theta, theta + 1)])


print("eps:", eps)
print("theta_f:", theta_f)
print("theta:", theta)
print("a:", a)
print()
print("prob(true):", prob(trv,trv))
print("prob(area):", area)
print("prob(others):", prob(0,trv))
print()
print("rr(true):", rr(trv,trv))
print("rr(other):", rr(0,trv))
print()

print("ratio:", prob(trv, trv) / prob(0,trv), np.exp(eps))
print("ratio rr:", rr(trv, trv) / rr(0,trv), np.exp(eps))

dist = np.array([prob(i, trv) for i in range(0,d)])
dist_rr = np.array([rr(i, trv) for i in range(0,d)])
print("sum(dist):", sum(dist))
print("sum(dist_rr):", sum(dist_rr))


# def euclid(x, y):                       # ground distance
# 	return abs(x-y)
# kant = qif.metric.kantorovich(euclid)   # distance on distributions

# d1 = np.array([1,0,0])
# d2 = np.array([0,0.5,0.5])
# print(kant(d1, d2))


#    a
#   ----        c = min { |i-x|, theta }
#   c(c-1)  

# %%
