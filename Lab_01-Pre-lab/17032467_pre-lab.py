import random
from itertools import accumulate

def fibonacci1(sl):
    if sl == 1:
        return 0
    elif sl == 2:
        return 1
    else:
        return fibonacci1(sl-2) + fibonacci1(sl-1)

def fibonacci2(sl):
    fib_seq = []
    for i in range(sl):
        if i == 0:
            fib_seq.append(0)
        elif i == 1:
            fib_seq.append(1)
        else:
            fib_seq.append(fib_seq[-2] + fib_seq[-1])
    return fib_seq

def tossCoin():
    head_chance = 0.2
    if random.random() < head_chance:
        headOrTail = "head"
    else:
        headOrTail = "tail"
    return headOrTail 

def chooseFromThree():
    option_A = 0.2
    option_B = 0.5
    option_C = 0.3
    options = list(accumulate([option_A, option_B, option_C]))
    chance = random.random()
    if chance < options[0]:
        selectedOption = "A"
    elif chance < options[1]:
        selectedOption = "B"
    else:
        selectedOption = "C"
    return selectedOption


if __name__ == "__main__":
    print(fibonacci2(10)) 
    
    print(tossCoin())

    print(chooseFromThree())