import random
import numpy as np

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



true_list = [random.randint(0,1) for _ in range(1000)]

random_respone_list = [random_respone(i) for i in true_list]


print("True sum: ", sum(true_list), "Randomized sum:", sum(random_respone_list))

