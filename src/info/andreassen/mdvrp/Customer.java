package info.andreassen.mdvrp;

public class Customer {
    public int id;
    public int x;
    public int y;
    public int serviceDuration;
    public int demand;

    public Customer(int id, int x, int y, int serviceDuration, int demand) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.serviceDuration = serviceDuration;
        this.demand = demand;
    }

}
