import numpy as np 
from random import randrange
import math

def fitness(individual, intervals, max_binary):
    fit = intervals[0] + int(individual, 2) * (intervals[1] - intervals[0]) / (max_binary - 1)
    max_fit = math.cos(fit) - math.sin(2.0 * fit)
    return fit, max_fit

def gen_population(size, N, intervals):
    pop = []
    nbits = '#0' + str(N+2) + 'b'
    max_binary = 2 ** N

    for i in range(size):
        individual = format(randrange(1,128), nbits)[2:]
        fit, max_fit = fitness(individual, intervals, max_binary)
        pop.append([individual, fit, max_fit])

    return pop 

def mutate(individual, intervals, N):
    start = randrange(0, N//2)
    end = randrange(N//2, N)
    
    out = individual[:start]
    for i in range(start, end, 1):
        if individual[i] == '0':
            out += '1'
        else:
            out += '0'
    out += individual[end:]
    fit, maxfit = fitness(out, intervals, 2**len(out))

    return out, fit, maxfit

def crossing(P, K, N, intervals):
    assert(K % 2 == 0)
    ids = [randrange(0,len(P)) for i in range(K)]
    tchildren = [P[i] for i in ids]

    #print("Before Cross Over: \n", tchildren)
    for i in range(len(tchildren)-1):
        cross_range = randrange(0, N-2) + 1

        #cross over
        tchildren[i][0] = tchildren[i][0][:cross_range] + P[ids[i+1]][0][cross_range:]
        tchildren[i+1][0] = tchildren[i+1][0][:cross_range] + P[ids[i]][0][cross_range:]

        #mutate these two guys and calculate their new fit scores
        tchildren[i][0], tchildren[i][1], tchildren[i][2] = mutate(tchildren[i][0], intervals, N)
        tchildren[i+1][0], tchildren[i+1][1], tchildren[i+1][2] = mutate(tchildren[i+1][0], intervals, N)

        #set the change in population if the progeny exceed the maximum fitness score of its parent
        if (P[ids[i]][2] < tchildren[i][1]):
            P[ids[i]] = tchildren[i]
        if (P[ids[i+1]][2] < tchildren[i+1][1]):
            P[ids[i+1]] = tchildren[i+1]

    #print("\nAfter Cross Over: \n", tchildren)

def main():
    intervals = (1, 6.423)
    pop = gen_population(30, 8, intervals)
    crossing(pop, 4, 8, intervals)

    #mutate population for 20 iterations
    e = 0 
    while (e < 20):
        #randomly mutate an individual
        id = randrange(0, 30)
        print("\nIndividual: {0} \nBefore Info.: \n{1}".format(id, pop[id]))
        pop[id][0], pop[id][1], pop[id][2] = mutate(pop[id][0], intervals, 8)
        print("After Info.: \n", pop[id])

        e+=1
main()