package info.andreassen.mdvrp;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public class Main {

    Customer[] customers;
    Depot[] depots;
    List<Chromosome> population;

    public Main() {

    }

    public void loadProblem(String path) {
        try(BufferedReader reader = new BufferedReader(new FileReader((path)))) {
            // Read initial data
            String[] firstLine = reader.readLine().split(" ");
            int maxVehicles = Integer.parseInt(firstLine[0]);
            int numCustomers = Integer.parseInt(firstLine[1]);
            int numDepots = Integer.parseInt(firstLine[2]);

            depots = new Depot[numDepots];
            customers = new Customer[numCustomers];

            // Get capacities for all depots
            for (int i = 0; i < numDepots; i++) {
                String[] depotLine = reader.readLine().strip().split("\\s+");
                int maxDuration = Integer.parseInt(depotLine[0]);
                int maxLoad = Integer.parseInt(depotLine[1]);
                depots[i] = new Depot(maxVehicles, maxDuration, maxLoad);
            }

            // Get data for all customers
            for (int i = 0; i < numCustomers; i++) {
                String[] customerLine = reader.readLine().strip().split("\\s+");
                int x = Integer.parseInt(customerLine[1]);
                int y = Integer.parseInt(customerLine[2]);
                int serviceDuration = Integer.parseInt(customerLine[3]);
                int demand = Integer.parseInt(customerLine[4]);

                customers[i] = new Customer(i + 1, x, y, serviceDuration, demand);
            }

            // Get positions of depots
            for (int i = 0; i < numDepots; i++) {
                String[] depotLine = reader.readLine().strip().split("\\s+");
                int x = Integer.parseInt(depotLine[1]);
                int y = Integer.parseInt(depotLine[2]);
                depots[i].x = x;
                depots[i].y = y;
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void cluster() {
        for (int i = 0; i < customers.length; i++) {
            int depot = 0;
            double closestDistance = -1;
            double nextClosest = -1;
            for (int j = 0; j < depots.length; j++) {
                double distance = Math.sqrt(Math.pow(customers[i].x - depots[j].x, 2) +
                                            Math.pow(customers[i].y - depots[j].y, 2));
                if (closestDistance == -1 || distance < closestDistance) {
                    nextClosest = closestDistance;
                    closestDistance = distance;
                    depot = j;
                } else if (nextClosest == -1) {
                    nextClosest = distance;
                }
            }

            depots[depot].initialCustomers.add(customers[i]);
        }
    }

    public void createInitialPopulation(int numChromosomes) {
        population = new ArrayList<>();

        // Initialize chromosome by simply shuffling the closest customers
        for (int i = 0; i < numChromosomes; i++) {
            Chromosome c = new Chromosome();
            for (int j = 0; j < depots.length; j++) {
                Collections.shuffle(depots[j].initialCustomers);
                List<Integer> depot = depots[j].initialCustomers.stream().map(x -> x.id).collect(Collectors.toList());
                c.depots.add(depot);
            }
            population.add(c);
        }
    }

    public static void main(String... args) {
        Main main = new Main();
        main.loadProblem("data/p01");
        main.cluster();
        main.createInitialPopulation(10);

        System.out.println("Boop");
    }
}
