package info.andreassen.mdvrp;

public class Customer {
    public int x;
    public int y;
    public int serviceDuration;
    public int demand;

    public Customer(int x, int y, int serviceDuration, int demand) {
        this.x = x;
        this.y = y;
        this.serviceDuration = serviceDuration;
        this.demand = demand;
    }

}
