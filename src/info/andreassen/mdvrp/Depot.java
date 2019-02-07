package info.andreassen.mdvrp;

import java.util.ArrayList;
import java.util.List;

public class Depot {
    public int maxVehicles;
    public int maxLoad;
    public int maxDuration;
    public int x;
    public int y;

    public List<Route> routes;

    public Depot(int x, int y, int maxVehicles, int maxDuration, int maxLoad) {
        this.x = x;
        this.y = y;
        this.maxVehicles = maxVehicles;
        this.maxDuration = maxDuration;
        this.maxLoad = maxLoad;

        this.routes = new ArrayList<>();
    }

    public Depot(int maxVehicles, int maxDuration, int maxLoad) {
        this(0, 0, maxVehicles, maxDuration, maxLoad);
    }
}
