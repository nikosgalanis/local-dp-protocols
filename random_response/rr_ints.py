import random

def random_respone(true_answer):
    first_coin = random.randint(0,1)
    if (first_coin == 0):
        return true_answer
    else:
        second_coin = random.randint(0,1)
        if (second_coin == 1):
            return 1
        else:
            return 0

real_sum = 0
dp_sum = 0

size = 100000
n_range = 200
# for count in range(size):

#     num = random.randint(0,n_range)
#     real_sum += num
#     string = "{0:e}".format(num)
#     l = [i for i in string]

#     response = ''.join([str(random_respone(i)) for i in l])
#     rr = int(response, 2)
#     dp_sum += rr

#     print(num, rr)
#     if (count % (size / 10) == 0):
#         print(count)

# print("True sum: ", real_sum / size, "Randomized sum:", dp_sum / size)


print("{0:e}".format(10))
