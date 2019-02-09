from random import shuffle, expovariate, random
from copy import deepcopy
import math

import matplotlib.pyplot as plt
import numpy as np

from data_classes import Depot, Customer
from utility import distance


population_size = 20

depots = None
customers = None
population = None


def load_problem(path):
    global depots, customers
    depots = []
    customers = []

    with open(path) as f:
        max_vehicles, num_customers, num_depots = tuple(map(lambda z: int(z), f.readline().strip().split()))

        for i in range(num_depots):
            max_duration, max_load = tuple(map(lambda z: int(z), f.readline().strip().split()))
            depots.append(Depot(max_vehicles, max_duration, max_load))

        for i in range(num_customers):
            vals = tuple(map(lambda z: int(z), f.readline().strip().split()))
            cid, x, y, service_duration, demand = (vals[j] for j in range(5))
            customers.append(Customer(cid, x, y, service_duration, demand))

        for i in range(num_depots):
            vals = tuple(map(lambda z: int(z), f.readline().strip().split()))
            cid, x, y = (vals[j] for j in range(3))
            depots[i].pos = (x, y)


def find_closest_depot(pos):
    closest_depot = None
    closest_distance = -1
    for depot in depots:
        d = distance(depot.pos, pos)
        if closest_depot is None or d < closest_distance:
            closest_depot = depot
            closest_distance = d

    return closest_depot, closest_distance


def plot(chromosome):
    for d, routes in enumerate(chromosome):
        depot = depots[d]
        for route in routes:
            positions = [depot.pos]
            last_pos = depot.pos
            for cid in route:
                last_pos = customers[cid - 1].pos
                positions.append(last_pos)
            positions.append(find_closest_depot(last_pos)[0].pos)

            positions = np.array(positions)
            plt.plot(positions[:, 0], positions[:, 1], zorder=0)

    depot_positions = np.array(list(map(lambda x: x.pos, depots)))
    customer_positions = np.array(list(map(lambda x: x.pos, customers)))
    plt.scatter(depot_positions[:, 0], depot_positions[:, 1], c='r', s=60, zorder=10)
    plt.scatter(customer_positions[:, 0], customer_positions[:, 1], c='k', s=20, zorder=20)

    plt.show()

if __name__ == '__main__':
    load_problem('../data/p01')
    plot(get_best())
