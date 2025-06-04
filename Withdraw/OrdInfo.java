public class OrdInfo {
    // 订单号/出金記録番号
    private String ordNo;

    // 提现类型/出金タイプ
    private String wcType;

    // 流水号/取引番号(送信の時使用)
    private String tradeNo;

    // 提现金额/出金金額
    private double wcAplAmt;

    // 提现执行银行/出金操作を実現する銀行
    private String rutCorg;

    // 目标银行/出金先カードの銀行
    private String capCorg;

    // 订单状态/出金状態
    private String tradeStatus;

    public OrdInfo(String ordNo, String wcType, double wcAplAmt, String rutCorg, String capCorg){
        this.ordNo = ordNo;
        this.wcType = wcType;
        this.tradeNo = "";
        this.wcAplAmt = wcAplAmt;
        this.rutCorg = rutCorg;
        this.capCorg = capCorg;
        this.tradeStatus = "W0";
    }

    // Getter

    public String getOrdNo() {
        return ordNo;
    }

    public String getWcType(){
        return wcType;
    }

    public String getTradeNo() {
        return tradeNo;
    }

    public double getWcAplAmt() {
        return wcAplAmt;
    }

    public String getRutCorg(){
        return rutCorg;
    }

    public String getCapCorg(){
        return capCorg;
    }

    public String getTradeStatus(){
        return tradeStatus;
    }

    // Setter

    public void setTradeNo(String tradeNo) {
        this.tradeNo = tradeNo;
    }

    public void setTradeStatus(String tradeStatus) {
        this.tradeStatus = tradeStatus;
    }

    // ToString

    @Override
    public String toString() {
        return "OrdInfo{" +
                "ordNo='" + ordNo + '\'' +
                ", wcType='" + wcType + '\'' +
                ", tradeNo='" + tradeNo + '\'' +
                ", wcAplAmt=" + wcAplAmt +
                ", rutCorg='" + rutCorg + '\'' +
                ", capCorg='" + capCorg + '\'' +
                ", tradeStatus='" + tradeStatus + '\'' +
                '}';
    }
}