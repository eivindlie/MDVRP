import random
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
    for i, depot in enumerate(depots):
        d = distance(depot.pos, pos)
        if closest_depot is None or d < closest_distance:
            closest_depot = (depot, i)
            closest_distance = d

    return closest_depot[0], closest_depot[1], closest_distance


def is_consistent_route(route, depot):
    route_load = 0
    route_duration = 0
    last_pos = depot.pos
    for c in route:
        customer = customers[c - 1]
        route_load += customer.demand
        route_duration += distance(last_pos, customer.pos) + customer.service_duration
        last_pos = customer.pos
    route_duration = find_closest_depot(last_pos)[2]

    return route_load < depot.max_load and (depot.max_duration == 0 or route_duration < depot.max_duration)


def initialize():
    groups = [[] for i in range(len(depots))]

    # Group customers to closest depot
    for c in customers:
        depot, depot_index, dist = find_closest_depot(c.pos)
        groups[depot_index].append(c.id)

    # Group customers in routes according to savings
    routes = [[] for i in range(len(depots))]
    for d in range(len(groups)):
        depot = depots[d]
        savings = []
        for i in range(len(groups[d])):
            ci = customers[groups[d][i] - 1]
            savings.append([])
            for j in range(len(groups[d])):
                if j <= i:
                    savings[i].append(0)
                else:
                    cj = customers[groups[d][j] - 1]
                    savings[i].append(distance(depot.pos, ci.pos) + distance(depot.pos, cj.pos) -
                                      distance(ci.pos, cj.pos))
        savings = np.array(savings)
        order = np.flip(np.argsort(savings, axis=None), 0)

        for saving in order:
            i = saving // len(groups[d])
            j = saving % len(groups[d])

            ci = groups[d][i]
            cj = groups[d][j]

            ri = -1
            rj = -1
            for r, route in enumerate(routes[d]):
                if ci in route:
                    ri = r
                if cj in route:
                    rj = r

            if ri == -1 and rj == -1:
                if len(routes[d]) < depot.max_vehicles:
                    route = [ci, cj]
                    if is_consistent_route(route, depot):
                        routes[d].append(route)
            elif ri != -1 and rj == -1:
                if routes[d][ri].index(ci) in (0, len(routes[d][ri]) - 1):
                    route = routes[d][ri] + [cj]
                    if is_consistent_route(route, depot):
                        routes[d][ri].append(cj)
            elif ri == -1 and rj != -1:
                if routes[d][rj].index(cj) in (0, len(routes[d][rj]) - 1):
                    route = routes[d][rj] + [ci]
                    if is_consistent_route(route, depot):
                        routes[d][rj].append(ci)
            elif ri != rj:
                route = routes[d][ri] + routes[d][rj]
                if is_consistent_route(route, depot):
                    if ri > rj:
                        routes[d].pop(ri)
                        routes[d].pop(rj)
                    else:
                        routes[d].pop(rj)
                        routes[d].pop(ri)
                    routes[d].append(route)

    # Order customers within routes
    for i, depot_routes in enumerate(routes):
        for j, route in enumerate(depot_routes):
            new_route = []
            prev_cust = random.choice(route)
            route.remove(prev_cust)
            new_route.append(prev_cust)

            while len(route):
                prev_cust = min(route, key=lambda x: distance(customers[x - 1].pos, customers[prev_cust - 1].pos))
                route.remove(prev_cust)
                new_route.append(prev_cust)
            routes[i][j] = new_route
    plot(routes)






def plot_map(show=True, annotate=True):
    depot_positions = np.array(list(map(lambda x: x.pos, depots)))
    customer_positions = np.array(list(map(lambda x: x.pos, customers)))

    depot_ids = np.arange(len(depots))
    customer_ids = np.arange(1, len(customers) + 1)

    depot_positions = np.array(list(map(lambda x: x.pos, depots)))
    customer_positions = np.array(list(map(lambda x: x.pos, customers)))
    plt.scatter(depot_positions[:, 0], depot_positions[:, 1], c='r', s=60, zorder=10)
    plt.scatter(customer_positions[:, 0], customer_positions[:, 1], c='k', s=20, zorder=20)

    if annotate:
        for i, id in enumerate(depot_ids):
            plt.annotate(id, depot_positions[i], zorder=30)
        for i, id in enumerate(customer_ids):
            plt.annotate(id, customer_positions[i], zorder=30)

    if show:
        plt.show()


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

    plot_map(False)

    plt.show()


if __name__ == '__main__':
    load_problem('../data/p01')
    plot_map()
    initialize()
