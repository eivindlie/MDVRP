package info.andreassen.mdvrp;

public class Codec {
    private Main main;

    public Codec(Main main) {
        this.main = main;
    }

    private double distanceToClosestDepot(Customer c) {
        double distance = -1;
        for (int i = 0; i < main.depots.length; i++) {
            double d = Math.sqrt(Math.pow(main.depots[i].x - c.x, 2) + Math.pow(main.depots[i].y - c.y, 2));
            if (distance == -1 || d < distance) {
                distance = d;
            }
        }

        return distance;
    }

    public double evaluate(Route route, Depot depot) {
        double distance = 0;
        for (int i = 0; i < route.customers.size(); i++) {
            Customer c1 = route.customers.get(i);
            if (i == 0) {
                distance += Math.sqrt(Math.pow(c1.x - depot.x, 2) + Math.pow(c1.y - depot.y, 2));
            } else {
                Customer c2 = route.customers.get(i - 1);
                distance += Math.sqrt(Math.pow(c1.x - c2.x, 2) + Math.pow(c1.y - c2.y, 2));
            }
        }

        distance += distanceToClosestDepot(route.customers.get(route.customers.size() - 1));

        return distance;
    }

    public void buildRoutes(Chromosome chromosome) {
        for (int i = 0; i < chromosome.depots.size(); i++) {
            Depot depot = main.depots[i];
            depot.routes.clear();
            int loadSum = 0;
            double durationSum = 0;

            Customer customer = null;
            Customer previousCustomer = null;
            depot.routes.add(new Route());
            for (int j = 0; j < chromosome.depots.get(i).size(); j++) {
                int c = chromosome.depots.get(i).get(j);
                previousCustomer = customer;
                customer = main.customers[c - 1];

                int prevX = (previousCustomer == null) ? depot.x : previousCustomer.x;
                int prevY = (previousCustomer == null) ? depot.y : previousCustomer.y;

                double customerDuration = Math.sqrt(Math.pow(customer.x - prevX, 2) + Math.pow(customer.y - prevY, 2));
                customerDuration += customer.serviceDuration;

                if (loadSum + customer.demand < depot.maxLoad &&
                        (durationSum + customerDuration) < depot.maxDuration || depot.maxDuration == 0) {
                    loadSum += customer.demand;
                    durationSum += customerDuration;
                } else {
                    loadSum = customer.demand;
                    durationSum = customer.demand;
                    depot.routes.add(new Route());
                }
                depot.routes.get(depot.routes.size() - 1).customers.add(customer);

                for (int k = 0; k < depot.routes.size() - 1; i++) {
                    Route r1 = depot.routes.get(k);
                    Route r2 = depot.routes.get(k + 1);

                    double dist1 = evaluate(r1, depot) + evaluate(r2, depot);
                    r2.customers.add(0, r1.customers.remove(r1.customers.size() - 1));
                    double dist2 = evaluate(r1, depot) + evaluate(r2, depot);

                    if (dist1 < dist2) {
                        r1.customers.add(r2.customers.remove(0));
                    }
                }
            }
        }
    }

    public double evaluate(Chromosome chromosome) {
        this.buildRoutes(chromosome);

        double distance = 0;
        for (int i = 0; i < main.depots.length; i++) {
            Depot depot = main.depots[i];
            for (Route route : depot.routes) {
                distance += evaluate(route, depot);
            }
        }

        return distance;
    }

}
