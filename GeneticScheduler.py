from math import floor
from random import choice, random, randint

from Details import get_details_instance
from utils import get_random_professor


class Chromosome:
    def __init__(self, gene, details):
        self.gene = gene
        self.courses_count = details.courses_count
        self.details = details
        self.fitness = Chromosome._update_fitness(gene, details)

    def mate(self, mate):
        pivot = randint(0, len(self.gene) - 1)
        gene1 = self.gene[:pivot] + mate.gene[pivot:]
        while not Chromosome(gene1, self.details).is_valid():
            pivot = randint(0, len(self.gene) - 1)
            gene1 = self.gene[:pivot] + mate.gene[pivot:]
        return Chromosome(gene1, self.details)

    def mutate(self, courses_profs):
        gene = list(self.gene)
        idx = randint(0, len(gene) - 1)
        try:
            gene[idx] = get_random_professor(idx % self.courses_count, courses_profs)
        except:
            return self.mutate(courses_profs)
        chromosome = Chromosome(gene, self.details)
        return chromosome if chromosome.is_valid() else self.mutate(courses_profs)

    def check_collision(self):
        num_of_batches = int(len(self.gene) / self.courses_count)
        for i in range(num_of_batches):
            profs = []
            for j in range(self.courses_count):
                if self.gene[i * self.courses_count + j] == -1:
                    continue
                if self.gene[i * self.courses_count + j] in profs:
                    return False
                profs.append(self.gene[i * self.courses_count + j])
        return True

    def check_single_offering(self):
        num_of_batches = int(len(self.gene) / self.courses_count)
        for i in range(self.courses_count):
            already_offered = False
            for j in range(num_of_batches):
                if self.gene[j * self.courses_count + i] == -1:
                    continue
                if already_offered is True:
                    return False
                already_offered = True
        return True

    def is_valid(self):
        if self.gene is None:
            return False
        return self.check_collision() and self.check_single_offering()

    @staticmethod
    def _update_fitness(gene, details):
        gene = list(gene)
        happiness = col_penalty = 0
        for i in range(len(gene)):
            if gene[i] != -1:
                happiness += details.courses_happiness[i % details.courses_count]

        for i in range(len(gene)):
            if i % details.courses_count == 0:
                offerings = []
            if gene[i] != -1:
                for offering in offerings:
                    col_penalty += details.collision_penalties[i % details.courses_count][offering]
                offerings.append(i % details.courses_count)

        return happiness - col_penalty

    @staticmethod
    def gen_random(details, skip=0.0):
        schedule = [-1 for i in range(details.days * details.slots * details.courses_count)]
        for i in range(details.courses_count):
            if random() < skip:
                continue
            slot = int(floor(random() * details.days * details.slots))
            while schedule[slot * details.courses_count + i] != -1:
                slot = int(floor(random() * details.days * details.slots))
            try:
                schedule[slot * details.courses_count + i] = get_random_professor(i, details.courses_profs)
            except:
                pass
        chromosome = Chromosome(schedule, details)
        return chromosome if chromosome.is_valid() else Chromosome.gen_random(details, skip + 0.05)


class Population:
    _tournamentSize = 3

    def __init__(self, size, crossover, elitism, mutation):
        self.size = size
        self.elitism = elitism
        self.mutation = mutation
        self.crossover = crossover
        self.details = get_details_instance()

        buf = []
        for i in range(size):
            buf.append(
                Chromosome.gen_random(self.details))
        self.population = list(sorted(buf, key=lambda x: x.fitness, reverse=True))

    def _tournament_selection(self):
        best = choice(self.population)
        for i in range(Population._tournamentSize):
            cont = choice(self.population)
            if cont.fitness > best.fitness:
                best = cont

        return best

    def _select_parents(self):
        return self._tournament_selection(), self._tournament_selection()

    def evolve(self):
        size = len(self.population)
        idx = int(round(size * self.elitism))
        buf = self.population[:idx]

        while idx < size:
            if random() <= self.crossover:
                (p1, p2) = self._select_parents()
                child = p1.mate(p2)
                if random() <= self.mutation:
                    buf.append(child.mutate(self.details.courses_profs))
                else:
                    buf.append(child)
                idx += 1
            else:
                if random() <= self.mutation:
                    buf.append(self.population[idx].mutate(self.details.courses_profs))
                else:
                    buf.append(self.population[idx])
                idx += 1

        self.population = list(sorted(buf[:size], key=lambda x: x.fitness, reverse=True))


if __name__ == "__main__":

    maxGenerations = 100
    pop = Population(size=100, crossover=0.8, elitism=0.05, mutation=0.3)

    for i in range(1, maxGenerations + 1):
        print("Generation %d: %s with fitness %d" % (i, pop.population[0].gene, pop.population[0].fitness))
        pop.evolve()

    details = pop.details
    for i, prof_num in enumerate(pop.population[0].gene):
        if prof_num != -1:
            day = floor(i / (details.courses_count * details.slots))
            slot = floor(i / details.courses_count) % details.slots
            course = i % details.courses_count
            print("{} {} {} {}".format(course + 1, prof_num + 1, day + 1, slot + 1))
