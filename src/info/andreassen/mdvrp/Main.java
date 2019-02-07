package info.andreassen.mdvrp;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class Main {

    Customer[] customers;
    Depot[] depots;

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

                customers[i] = new Customer(x, y, serviceDuration, demand);
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

    public void initialize() {
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

    public static void main(String... args) {
        Main main = new Main();
        main.loadProblem("data/p01");
        main.initialize();

        System.out.println("Boop");
    }
}
