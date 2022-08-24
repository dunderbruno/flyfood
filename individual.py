'''
classe Individual

Representa um indivíduo da população.
Cada indivíduo equivale a um trajeto possível.
'''

import random


class Individual():
    def __init__(self, dna, r, fitness_value):
        self.dna = dna
        self.r = r
        self.fitness_value = fitness_value
        self.distance = self.calculate_distance()
        

    def __repr__(self):
        letras = [i[2] for i in self.dna]
        letras_coladas = ''.join(letras)
        return str(letras_coladas) + ' : ' + str(self.distance)


    def __lt__(self, other):
        return self.distance < other.distance


    def calculate_distance(self):
        initial_distance = abs(self.dna[0][0] - self.r[0]) + abs(self.dna[0][1] - self.r[1])

        middle_distance = 0
        for index in range(len(self.dna)):
            if index+1 < len(self.dna):
                middle_distance += abs(self.dna[index+1][0] - self.dna[index][0]) + abs(self.dna[index+1][1] - self.dna[index][1])

        last_mile = abs(self.dna[index][0] - self.r[0]) + abs(self.dna[index][1] - self.r[1])

        distance = initial_distance + middle_distance + last_mile

        return distance


    def get_distance(self):
        return f"Distância para o trajeto {self.distance}"


    def mutate(self):
        
        value_a = random.choice(self.dna)
        index_a = self.dna.index(value_a)

        value_b = random.choice(self.dna)
        index_b = self.dna.index(value_b)

        self.dna[index_a] = value_b
        self.dna[index_b] = value_a

        self.distance =  self.calculate_distance()
