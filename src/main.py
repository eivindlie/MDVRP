from random import shuffle, expovariate, random
import math

from data_classes import Depot, Customer
from utility import distance


population_size = 100

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
        for route in routify(chromosome[depot_index], depot):
            customer = None
            last_pos = depot.pos
            for cid in route:
                customer = customers[cid - 1]
                score += distance(last_pos, customer.pos)
                score += customer.service_duration
            score += find_closest_depot(customer.pos)[1]
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
    return d


def create_initial_population():
    global population
    population = []

    for i in range(population_size):
        chromosome = []
        for depot in depots:
            shuffle(depot.closest_customers)
            d = list(map(lambda x: x.id, depot.closest_customers[:]))
            # d = routify(depot.closest_customers, depot)
            chromosome.append(d)
        population.append(chromosome)


def reproduce(elitism=2):
    global population
    population.sort(key=lambda p: evaluate(p))
    new_population = []

    # Directly transfer the best chromosomes
    for i in range(elitism):
        new_population.append(population[i])

    for i in range(math.ceil((population_size - elitism) / 2)):
        parents = []
        for j in range(2):
            # Use an exponential distribution, which is more likely to draw the best chromosomes
            p = int(expovariate(1/((population_size / 2) - 2))) % population_size
            parents.append(population[p])

        # TODO Implement crossover
        new_population.extend(parents)
    population = new_population


def mutate(rate=0.01):
    for chromosome in population:
        if random() > rate:
            continue

        sel = random()

        if sel < 0.3:
            # Reverse a cut from the chromosome
            depot_index = int(random() * len(chromosome))
            depot = chromosome[depot_index]
            if not len(depot):
                continue
            cut1 = int(random() * len(depot))
            cut2 = cut1 + int(random() * (len(depot) - cut1))

            chromosome[depot_index] = depot[:cut1] + depot[cut2-1:cut1-1:-1] + depot[cut2:]


def train(generations):
    for i in range(generations):
        if i % 10 == 0:
            best_score = min(map(lambda x: evaluate(x), population))
            print(f'[Generation {i}] Best score: {best_score}')

        reproduce()
        mutate()


if __name__ == '__main__':
    load_problem('../data/p06')
    cluster()
    create_initial_population()

    train(1000)
