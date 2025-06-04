public class UserInfo {

    // 姓名/名前
    private String name;

    // 余额/残高
    private double balance;

    public UserInfo(String name, double balance){
        this.name = name;
        this.balance = balance;
    }

    // Getter
    public String getName() {
        return name;
    }

    public double getBalance() {
        return balance;
    }

    // Setter
    public void setBalance(double balance) {
        this.balance = balance;
    }

    @Override
    public String toString() {
        return "UserInfo{" +
                "name='" + name + '\'' +
                ", balance=" + balance +
                '}';
    }
}
