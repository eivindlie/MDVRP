from random import shuffle, expovariate, random
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


def cluster():
    for customer in customers:
        closest_depot, _ = find_closest_depot(customer.pos)

        closest_depot.closest_customers.append(customer)


def find_closest_depot(pos):
    closest_depot = None
    closest_distance = -1
    for depot in depots:
        d = distance(depot.pos, pos)
        if closest_depot is None or d < closest_distance:
            closest_depot = depot
            closest_distance = d

    return closest_depot, closest_distance


def evaluate(chromosome):
    score = 0
    for depot_index in range(len(chromosome)):
        depot = depots[depot_index]
        for route in chromosome[depot_index]:
            if len(route) == 0:
                continue
            route_load = 0
            route_length = 0
            customer = None
            last_pos = depot.pos
            for cid in route:
                customer = customers[cid - 1]
                route_load += customer.demand
                route_length += distance(last_pos, customer.pos)
                route_length += customer.service_duration
            route_length += find_closest_depot(customer.pos)[1]
            score += route_length

            if route_load > depot.max_load or (depot.max_duration != 0 and route_length > depot.max_duration):
                return math.inf
    return score


def routify(cust, depot):
    d = []
    route = []
    route_load = 0
    route_distance = 0
    last_pos = depot.pos
    for cid in cust:
        customer = customers[cid - 1]
        _, return_distance = find_closest_depot(customer.pos)
        travel_distance = distance(last_pos, customer.pos)
        if route_load + customer.demand < depot.max_load \
                and (depot.max_duration == 0
                     or travel_distance + customer.service_duration + return_distance < depot.max_duration):
            route_distance += travel_distance + customer.service_duration
            route_load += customer.demand
            route.append(customer.id)
        else:
            # assert len(d) < depot.max_vehicles, 'No more vehicles available - ' \
            #                                    'too many customers assigned to depot'
            d.append(route)
            route_distance = distance(customer.pos, depot.pos) + customer.service_duration
            route_load = customer.demand
            route = [customer.id]
        last_pos = customer.pos
    d.append(route)
    while len(d) < depot.max_vehicles:
        d.append([])

    return d


def create_initial_population():
    global population
    population = []

    for i in range(population_size):
        chromosome = []
        for depot in depots:
            shuffle(depot.closest_customers)
            d = list(map(lambda x: x.id, depot.closest_customers[:]))
            d = routify(d, depot)
            chromosome.append(d)
        population.append(chromosome)


def reproduce(elitism=2):
    global population
    population.sort(key=lambda p: evaluate(p))
    new_population = []

    # Directly transfer the best chromosomes
    for i in range(elitism):
        new_population.append(population[i])

    while len(new_population) < population_size:
        parents = []
        for j in range(2):
            # Use an exponential distribution, which is more likely to draw the best chromosomes
            p = int(expovariate(1/((population_size / 2) - 2))) % population_size
            parents.append(population[p])

        d = int(random() * len(depots))
        r1 = int(random() * len(parents[0][d]))
        r2 = int(random() * len(parents[1][d]))

        new_population.extend(parents)
    population = new_population[:population_size]


def mutate(rate=0.3):
    for chromosome in population:
        if random() > rate:
            continue

        sel = random()

        if sel < 0.01:
            # Reverse a cut from the chromosome
            depot_index = int(random() * len(chromosome))
            depot = [customer for route in chromosome[depot_index] for customer in route]
            if not len(depot):
                continue
            cut1 = int(random() * len(depot))
            cut2 = cut1 + int(random() * (len(depot) - cut1 + 1))
            if cut1 == 0:
                depot = depot[:cut1] + depot[cut2-1::-1] + depot[cut2:]
            else:
                depot = depot[:cut1] + depot[cut2-1:cut1-1:-1] + depot[cut2:]

            chromosome[depot_index] = routify(depot, depots[depot_index])

        elif sel < 0.99:
            # Select single customer, and insert at best possible location
            depot_index = int(random() * len(chromosome))
            depot = chromosome[depot_index]
            if len(depot) == 0:
                continue

            route_index = int(random() * len(depot))
            route = depot[route_index]

            if len(route) == 0:
                continue

            customer_index = int(random() * len(route))
            customer = route.pop(customer_index)

            best_index = None
            best_score = -1
            for i in range(len(depot)):
                for j in range(len(depot[i]) + 1):
                    depot[i].insert(j, customer)
                    score = evaluate(chromosome)

                    if best_index is None or score < best_score:
                        best_index = (i, j)
                        best_score = score

                    depot[i].pop(j)

            depot[best_index[0]].insert(best_index[1], customer)
        else:
            # Swap two customers
            depot_index = int(random() * len(chromosome))
            depot = chromosome[depot_index]
            if len(depot) == 0:
                continue

            r1 = int(random() * len(depot))
            r2 = int(random() * len(depot))

            if len(depot[r1]) == 0 or len(depot[r2]) == 0:
                continue

            c1 = int(random() * len(depot[r1]))
            c2 = int(random() * len(depot[r2]))

            depot[r1][c1], depot[r2][c2] = depot[r2][c2], depot[r1][c1]
            if evaluate(chromosome) == math.inf:
                # Swap back if new chromosome is illegal
                depot[r1][c1], depot[r2][c2] = depot[r2][c2], depot[r1][c1]


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


def get_best():
    return min(population, key=lambda x: evaluate(x))


def train(generations):
    for i in range(generations):
        if i % 10 == 0:
            best_score = min(map(lambda x: evaluate(x), population))
            print(f'[Generation {i}] Best score: {best_score}')

        reproduce()
        mutate()


if __name__ == '__main__':
    load_problem('../data/p01')
    cluster()
    create_initial_population()

    train(1000)
    plot(get_best())
