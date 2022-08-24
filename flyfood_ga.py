'''
Resolução do problema do caixeiro viajante pelo método de Computação Evolutiva

Autor: Bruno Olimpio dos Santos
'''

import random
import string
import sys
from math import factorial

from individual import Individual


def create_weights_array():
    # Cria matriz de pesos para método da roleta
    array = []
    original_slot_size = int(len(population)/4)
    weight = 0.5
    
    a = 0
    b = original_slot_size
    
    for x in range(len(population)):
        if x < b:
            array.append(weight)
        else:
            weight = weight/2
            array.append(weight)
            a = b
            b = b + original_slot_size
    return array


def tournament(population, population_size, weights_array): 
    # Executa torneio usanto o método da roleta
    winners = []
    for t in range(population_size):
        player1 = random.choices(population, weights_array)
        player2 = random.choices(population, weights_array)

        if player1 > player2:
           winners.append(player1)
        else:
           winners.append(player2)

    return winners


def crossing(r, parent1, parent2, values):
    for x in range(int(len(parent1.dna)/2)):
        values.append(random.choice(parent1.dna))

    positions = []
    for v in values:
        for p in range(len(parent2.dna)):
            if parent2.dna[p][2] == v[2]:
                positions.append(p)

    child_dna = []
    for d in range(len(parent1.dna)):
        if d in positions:
            child_dna.append(None)
        else:
            child_dna.append(parent1.dna[d])

    complement = child_dna[:]
    for x in parent2.dna:
        if x not in child_dna:
            index = complement.index(None)
            complement[index] = x

    child = Individual(complement[:],r,0)

    return child


def reproduction(r, winners):
    childs = []

    for w in range(int(len(winners)/2)):
        parent1 = winners[w][0]
        parent2 = winners[w+int(len(winners)/2)-1][0]
        values = []
    
        child1 = crossing(r, parent1, parent2, values)
        childs.append(child1)
        child2 = crossing(r, parent2, parent1, values)
        childs.append(child2)

    return childs


def mutation(population):
    for i in population:
        i.mutate()


number_of_generations = int(sys.argv[1])
population_size = int(sys.argv[2])
filename = sys.argv[3]

file = f"maps/{filename}.txt"


with open(file, 'r') as input:
    first_line = input.readline()
    side_a = int(first_line[0])
    side_b = int(first_line[1])
    matrix = input.readlines()


longest_route = ((side_a * side_b)*2)-2
print(longest_route)


lines = [[j for j in i.strip('\n')] for i in matrix]
r = None
points = []
for y, line in enumerate(lines):
    for x, value in enumerate(line):
        if value == 'R':
            r = (x, y, value)
        elif (value != 'R') and (value in string.ascii_uppercase):
            points.append((x, y, value))

number_of_points = len(points)
population = []


if factorial(number_of_points) < 100:
    population_size = factorial(number_of_points)


for i in range(population_size):
    random.shuffle(points)
    individual = Individual(points[:],r,0)
    while True:
        if individual.distance >= longest_route:
            random.shuffle(points)
            individual = Individual(points[:],r,0)
        else:
            break
    population.append(individual)


population = sorted(population)
weights_array = create_weights_array()
best_route = max(population) # valor de referência para uso posterior em comparações

print(f"Maior trajeto na população inicial: ")
print(best_route)
print('\n')

counter = 1
while True:
    winners = tournament(population, population_size, weights_array)
    generation = reproduction(r, winners)
    mutation(generation)
    smaller = min(generation)

    if smaller < best_route:
        best_route = smaller
        print(f"{smaller} na geração {counter}")

    counter += 1
    if counter == number_of_generations:
        break
    else:
        population = generation
