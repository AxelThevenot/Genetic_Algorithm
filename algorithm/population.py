from individual import *


class Population:

    def __init__(self, size, pointList):
        """
        Initialize population of size individuals from a pointList
        :param size: size of the population
        :param pointList: pointList from which the individuals are made from
        """
        self.size = size
        # randomly create individuals from pointList
        self.individuals = [Individual(random.sample(pointList, len(pointList)))
                                       for _ in range(self.size)]
        self.best = self.individuals[0]

    def newIndividuals(self):
        """
        Create a random new Individual while the population size is not equal to the size chosen
        """
        while len(self.individuals) < self.size:
            points = self.individuals[0].points
            new_individual = Individual(random.sample(points, len(points)))
            self.individuals.append(new_individual)

    def sort(self):
        """
        sort the individuals according to their cost
        """
        self.individuals.sort(key=lambda individual: individual.cost)
        # change the best individuals if the new best one beats the latest one
        if self.best.cost >= self.individuals[0].cost:
            self.best = self.individuals[0]

    # region genetic
    def selection(self, ratio_selection):
        """
        The selection here is to keep the ratio_selection% bests
        :param ratio_selection: selection ratio interested in
        """
        self.individuals = [self.individuals[individual]
                            for individual in range(int(ratio_selection*len(self.individuals)))]

    def crossover(self, ratio_crossover, ratio_selection):
        """
        Crossover the selected individuals
        :param ratio_crossover: child ratio from crossover interested in
        :param ratio_selection: selection ratio interested in
        """
        # count the number of parents after the selection
        potential_parent_count = int(ratio_selection * self.size - 1)
        for _ in range(int(ratio_crossover * self.size)):
            # select a first parent
            parent_1_index = random.randint(0,potential_parent_count)
            # select a second parent (different than the first one)
            parent_2_index = random.randint(0,potential_parent_count)
            # verify they are different or change the second parent
            while parent_1_index == parent_2_index:
                parent_2_index = random.randint(0, potential_parent_count)
            self.individuals.append(self.individuals[parent_1_index].crossWith(self.individuals[parent_2_index]))

    def mutation(self, ratio_mutation):
        """
        Mutate randomly the population according to the ratio chosen
        :param ratio_mutation: mutation ratio interested in
        """
        for _ in range(int(ratio_mutation * self.size)):
            # select a random individual
            individual_index = random.randint(0, self.size - 1)
            self.individuals[individual_index].mutate()

    def nextGeneration(self, ratio_selection, ratio_crossover, ratio_mutation):
        """
        Next generation process
        :param ratio_selection: selection ratio interested in
        :param ratio_crossover: child ratio from crossover interested in
        :param ratio_mutation: mutation ratio interested in
        """
        self.sort()  # sort the individuals according to their cost
        self.selection(ratio_selection)  # selection process according to the ratio chosen
        self.crossover(ratio_crossover, ratio_selection)  # crossover process according to the ratio chosen
        self.newIndividuals()  # create new individuals if needed
        self.mutation(ratio_mutation)  # mutation process according to the ratio chosen
    # endregion


def randomPopulation(size_population, size_plot, n_point):
    """
    Create a new random population
    :param size_population: size of population
    :param size_plot: size of the plot side
    :param n_point: number of point each individuals is made from
    :return: population created
    """
    # create a random array of point to define a new individual
    points = [(random.random() * size_plot, random.random() * size_plot)
              for _ in range(n_point)]
    return Population(size_population, points)
