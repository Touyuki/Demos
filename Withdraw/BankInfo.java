public class BankInfo {

    // 姓名/名前
    private String name;

    // 余额/残高
    private double balance;

    // 银行信息类/銀行情報クラス
    public BankInfo(String name, double balance){
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
