import numpy as np
from matplotlib import pyplot as plt
import random

def bin2gray(binary):
    binary = list(binary)
    gray = [binary[0]]
    for i in range(1, len(binary)):
        if (binary[i-1] == binary[i]):
            gray.append(0)
        else:
            gray.append(1)
    return ''.join(map(lambda x: str(x), gray))

def calcHamming(code1, code2):

    # pad binary strings with leading zeroes if necessary
    code1 = str(code1)
    code2 = str(code2)
    if len(code1) > len(code2):
        code2 = code2.zfill(len(code1))
    else:
        code1 = code1.zfill(len(code2))
    
    # intialize count
    count = 0
    for i in range(len(code1)):
        if code1[i] != code2[i]:
            count += 1
    return count

# convert to gray code
binary = np.binary_repr(7)
print("7 in binary:", bin2gray(binary))

# calc hamming distance
print("Hamming distance between 1001 and 1:", calcHamming(1001, 1))

# convert decimal to binary
decimal_list = list(range(1, 11))
binary_list = list(map(lambda x: np.binary_repr(x), decimal_list))
bin_hamming_dist = list(map(lambda x, y: calcHamming(x, y), binary_list[:-1], binary_list[1:]))
bin_hamming_dist.insert(0, 0)

gray_list = list(map(lambda x: bin2gray(x), binary_list))
gray_hamming_dist = list(map(lambda x, y: calcHamming(x, y), gray_list[:-1], gray_list[1:]))
gray_hamming_dist.insert(0, 0)

plt.figure('Binary code hamming distance')
plt.plot(binary_list, bin_hamming_dist, marker='o')
plt.ylabel("Hamming count")
plt.xlabel("Binary code")
plt.yticks(ticks=range(0, 4), labels=range(0,4))

plt.figure('Gray code hamming distance')
plt.plot(gray_list, gray_hamming_dist, marker='o')
plt.ylabel("Hamming count")
plt.xlabel("Gray code")
plt.yticks(ticks=range(0, 4), labels=range(0,4))

# optimization

def value2gray(value):
    return bin2gray(np.binary_repr(value))

def gray2bin(gray):
    gray = list(gray)
    binary = [gray[0]]
    for i in range(1, len(gray)):
        if binary[i-1] == gray[i]:
            binary.append("0")
        else:
            binary.append("1")
    return ''.join(binary)

def bin2decimal(binary):
    binary = list(str(binary))
    length = len(binary)
    # initialize decimal
    decimal = 0
    for i in range(length):
        length -= 1
        decimal += (2**length) * int(binary[i])
    return decimal

def gray2value(gray):
    return bin2decimal(gray2bin(gray))

def generatePopulation(pop_size, pop_min, pop_max):
    # this function generate the first generation randomly based on the 
    # population size and the range of the value of each chromosome
    return [random.randint(pop_min, pop_max) for i in range(pop_size)]

def calculateFitness(value):
    return value

def selectParents(chromosomes, pop_size):
    parent_pairs = []
    for i in range(int(pop_size/2)):
        parent_pairs.append(random.sample(chromosomes, k=2))
    return parent_pairs

def crossover(parents):
    parents = [value2gray(parent) for parent in parents]
    half = int(len(parents[0])/2)
    offsprings = [parents[0][:half]+parents[1][half:], parents[1][:half]+parents[0][half:]]
    offsprings = [gray2value(offspr) for offspr in offsprings]
    return offsprings

def mutate(chromosome, p_mutation):
    # this function mutates each gene of a chromosome based on the mutation probability
    chromosome_gray = value2gray(chromosome)
    inverted_bit = '1' if chromosome_gray[-1] == '0' else '0'
    mutated_gray = chromosome_gray[:-1] + inverted_bit
    mutated = gray2value(mutated_gray)
    if (random.random() < p_mutation):
        return mutated
    return chromosome

def findOverallDistance(chromosomes):
    # this function takes the input of the current population and returns the overall 
    # distance among fitnesses of all chromosomes
    mean = sum(chromosomes)/len(chromosomes)
    overall_distance = sum([abs(mean - chromos) for chromos in chromosomes])
    return overall_distance

if __name__ == "test":
    print(mutate(15, 0.1))


if __name__ == "__main__":
    # main function
    ## parameter definition
    pop_size = 10
    pop_min = 1 #1cm
    pop_max = 10 #10cm
    curr_iter = 0
    max_iter = 100
    min_overalldistance = 0.5
    p_mutation = 0.05
    ## initialise population
    population = []
    population.append(generatePopulation(pop_size, pop_min, pop_max))
    while (curr_iter < max_iter and findOverallDistance(population[-1]) > min_overalldistance):
        curr_iter += 1
        ## select parent pairs
        parents = selectParents(population[-1], len(population[-1]))
        ## perform crossover
        offsprings = []
        for p in parents:
            new_offsprings = crossover(p)
            for o in new_offsprings:
                offsprings.append(o)
        ## perform mutation
        mutated = [mutate(offspring, p_mutation) for offspring in offsprings]
        ## update current population
        population.append(mutated)
    print(population)