import random

class Individual:

    def __init__(self, _points):
        """
        Initialize a individual from a list of point
        :param _points: list of point the individual is made from
        """
        self.points = [list(point) for _, point in enumerate(_points)]
        self.cost = self.costFunction()

    def toXY(self):
        """
        to return X and Y array of coordinates to plot the individual
        :return: X coordinates, Y coordinates
        """
        # isolate the X and the Y array to return them
        X = [self.points[p][0] for p in range(len(self.points))]
        Y = [self.points[p][1] for p in range(len(self.points))]
        # as the starting point is (0, 0) point, we are looking to the first nearest point
        minDistance = {"index": 0, "distance": X[0] ** 2 + Y[0] ** 2}  # dictionary to easy use
        for i in range(len(X)):
            distance_i = X[i] ** 2 + Y[i] ** 2  # take the distance from (0, 0) f each point
            if distance_i < minDistance["distance"]:  # compare to the best point already found
                # replace it if there is a new nearest point from (0, 0)
                minDistance["index"] = i
                minDistance["distance"] = distance_i

        # surround X, Y by the starting point (0, 0), which is also the ending point
        X = [0] + X[minDistance["index"]:] + X[:minDistance["index"]] + [0]
        Y = [0] + Y[minDistance["index"]:] + Y[:minDistance["index"]] + [0]
        return X, Y

    # region genetic
    def costFunction(self):
        """
        Calculate the distance needed to link each point
        :return:
        """

        # only create the distance function between two points (Pythagoras)
        def distance(point_1, point_2):
            return (point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2

        # and sum the distances between each point to have the cost value
        cost = 0
        for i in range(len(self.points) - 1):
            cost += distance(self.points[i], self.points[(i + 1)])
        return cost

    def breedWith(self, other):
        """
        breed self with other as a 4-points crossover
        :param other: other individuals
        :return: child
        """
        # select randomly the 4-point of te crossover
        genes = [random.randint(0, len(self.points) - 1) for _ in range(4)]
        genes.sort()  # sort them for the use

        points_from_self = self.points[genes[0]:genes[1]]  # first part of self's points
        points_from_self += self.points[genes[2]:genes[3]]  # second part of self's points
        # looking for the missing points
        points_from_other = [point for _, point in enumerate(other.points) if point not in points_from_self]

        # add the parent's point to create the child's list of point
        child_points = points_from_self + points_from_other
        return Individual(child_points)

    def mutate(self):
        """
        mutate an individual
        """
        # select a random gene
        rand_index = random.randint(0, len(self.points) - 1)
        # mutate [a, b, c, d, e, f, g] with rand_index = 2 become [c, d, e, f, g, a, b,]
        point_mutated = self.points[rand_index:]  # [c, d, e, f, g] in the example
        point_mutated += self.points[:rand_index]  # add [a, b] in the example
        self.points = point_mutated[:]
    # endregion

