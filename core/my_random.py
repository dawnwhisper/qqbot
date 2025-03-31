import random

def random_choice(seq, prob, k=1) -> list:
    res = []
    for j in range(k):
        p = random.random()
        for i in range(len(seq)):
            if sum(prob[:i]) < p <= sum(prob[:i+1]):
                res.append(seq[i])
    return res

def get_random_num(a=1, b=100) -> int:
    return random.randint(a,b)