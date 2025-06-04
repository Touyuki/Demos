import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Random;

public class Withdraw_Process extends JFrame {
    private JLabel balanceValue1, balanceValue2, balanceValue3, balanceValue4;
    private JLabel bankValue1,bankValue2,bankValue3,bankValue4;
    private JLabel tradeNoValue1, tradeNoValue2, tradeNoValue3, tradeNoValue4;
    private JLabel tradeStatusValue1,tradeStatusValue2,tradeStatusValue3,tradeStatusValue4;
    private JTextArea messageBox1, messageBox2, messageBox3, messageBox4;

    public Withdraw_Process() {
        // 设置窗口标题/GUIタイトルを設定
        super("出金システム(機能説明用)");

        // 新建提现单 wcType 40:一般用户提现/ 出金記録の新規作成　wcType 40:一般口座からの出金
        OrdInfo ordInfo = new OrdInfo("620418234561","40", 20.00, "ICBC", "ABC");

        // 新建用户/ユーザーの初期化
        UserInfo userInfo = new UserInfo("張xx",100.00);

        // 新建银行用户/銀行口座の初期化
        BankInfo bankInfo = new BankInfo("張xx",0.00);

        // 设置窗口大小/GUIウインドウサイズ設定
        setSize(550, 500);

        // 设置关闭操作/GUI終了機能
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // 创建主面板/メイン画面の新規作成
        JPanel mainPanel = new JPanel(new BorderLayout());

        // 创建标签页面板/タブ画面作成用クラス
        JTabbedPane tabbedPane = new JTabbedPane();

        // 全局变量初始化/グローバル変数の初期化
        globalVarProcess(ordInfo,userInfo, bankInfo);

        // 添加第一个标签页/一個目のタブ画面の宣言と設定
        JPanel tab1 = createInitialProcessTab(userInfo, bankInfo,ordInfo);
        tabbedPane.addTab("初期処理", null, tab1, "初期処理");

        // 添加第二个标签页/二個目のタブ画面の宣言と設定
        JPanel tab2 = createPrepareProcessTab(userInfo, bankInfo,ordInfo);
        tabbedPane.addTab("出金準備", null, tab2, "出金準備");

        // 添加第三个标签页/三個目のタブ画面の宣言と設定
        JPanel tab3 = createSendingProcessTab(userInfo, bankInfo, ordInfo);
        tabbedPane.addTab("出金指令送信", null, tab3, "出金指令送信");

        // 添加第四个标签页/四個目のタブ画面の宣言と設定
        JPanel tab4 = createResultConfirmTab(userInfo, bankInfo, ordInfo);
        tabbedPane.addTab("結果確認", null, tab4, "結果確認");

        // 将标签页添加到主面板/タブ設定クラスをメイン画面に追加
        mainPanel.add(tabbedPane, BorderLayout.CENTER);

        // 添加主面板到窗口/メイン画面を設定
        add(mainPanel);

        // 显示窗口/GUI表示設定
        setVisible(true);
    }

    // 创建第一个标签页（初期处理）/一個目のタブ画面を作成(初期処理)
    private JPanel createInitialProcessTab(UserInfo userInfo, BankInfo bankInfo, OrdInfo ordInfo) {

        JPanel panel = new JPanel(new GridBagLayout());

        // 共同处理 GUI/ GUI設定の共通処理
        publicProcess(userInfo,bankInfo,ordInfo,panel,balanceValue1,bankValue1,tradeNoValue1,tradeStatusValue1);

        // 消息栏/メッセージ欄
        messageBox1.setEditable(false);
        messageBox1.setLineWrap(true);
        messageBox1.setWrapStyleWord(true);
        messageBox1.setBounds(30,230,450,120);
        panel.add(messageBox1);

        // 按钮/ボタン
        JButton button = new JButton("初期処理");
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

                if(ordInfo.getTradeStatus().equals("W0")) {
                    ordInfo.setTradeStatus("W1");
                    tradeStatusValue1.setText("W1");

                    // 其他页面的修改/その他タブ画面の修正
                    tradeStatusValue2.setText("W1");
                    tradeStatusValue3.setText("W1");
                    tradeStatusValue4.setText("W1");

                    messageBox1.setText("");
                    messageBox1.append("初期処理(記帳)が終わりました。");
                }
                else{
                    messageBox1.setText("");
                }
            }
        });

        button.setBounds(50,390,120,30);
        panel.add(button);

        JButton button1 = new JButton("初期化(機能説明用)");
        button1.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                messageBox1.setText("");
                ordInfo.setTradeNo("");
                ordInfo.setTradeStatus("W0");
                userInfo.setBalance(100.00);
                bankInfo.setBalance(0.00);

                tradeStatusValue1.setText("W0");
                tradeNoValue1.setText("");
                balanceValue1.setText(String.format("%.2f", userInfo.getBalance()) + " 元");
                bankValue1.setText(String.format("%.2f", bankInfo.getBalance())+ " 元");
                // 其他页面的修改

                tradeStatusValue2.setText("W0");
                tradeNoValue2.setText("");
                balanceValue2.setText(String.format("%.2f", userInfo.getBalance()) + " 元");
                bankValue2.setText(String.format("%.2f", bankInfo.getBalance())+ " 元");
                messageBox2.setText("");

                tradeStatusValue3.setText("W0");
                tradeNoValue3.setText("");
                balanceValue3.setText(String.format("%.2f", userInfo.getBalance()) + " 元");
                bankValue3.setText(String.format("%.2f", bankInfo.getBalance())+ " 元");
                messageBox3.setText("");

                tradeStatusValue4.setText("W0");
                tradeNoValue4.setText("");
                balanceValue4.setText(String.format("%.2f", userInfo.getBalance()) + " 元");
                bankValue4.setText(String.format("%.2f", bankInfo.getBalance())+ " 元");
                messageBox4.setText("");}
        });
        button1.setBounds(200,390,160,30);
        panel.add(button1);

        return panel;
    }

    // 创建第二个标签页（流水号生成）/二個目のタブ画面の宣言と設定(出金準備)
    private JPanel createPrepareProcessTab(UserInfo userInfo, BankInfo bankInfo, OrdInfo ordInfo){

        JPanel panel = new JPanel(new GridBagLayout());

        // 共同处理 GUI / GUI設定の共通処理
        publicProcess(userInfo,bankInfo,ordInfo,panel,balanceValue2,bankValue2,tradeNoValue2,tradeStatusValue2);

        // 消息栏/メッセージ欄
        messageBox2.setEditable(false);
        messageBox2.setLineWrap(true);
        messageBox2.setWrapStyleWord(true);
        messageBox2.setBounds(30,230,450,120);
        panel.add(messageBox2);

        // 按钮/ボタン
        JButton button = new JButton("出金準備");
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

                if(ordInfo.getTradeStatus().equals("W1")) {
                    ordInfo.setTradeStatus("W2");
                    tradeStatusValue2.setText("W2");

                    // 其他页面的修改/その他タブ画面の変更
                    tradeStatusValue1.setText("W2");
                    tradeStatusValue3.setText("W2");
                    tradeStatusValue4.setText("W2");

                    messageBox2.setText("");
                    messageBox2.append("出金準備が終わりました。");

                    // 流水号生成/取引番号の作成
                    SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMddHHmmss");
                    String part1 = sdf.format(new Date());
                    Random random = new Random();
                    StringBuilder sb = new StringBuilder();
                    for (int i = 0; i < 6; i++) {
                        sb.append(random.nextInt(10));
                    }
                    String part2 = sb.toString();
                    ordInfo.setTradeNo(part1+part2);
                    tradeNoValue2.setText(ordInfo.getTradeNo());

                    tradeNoValue1.setText(ordInfo.getTradeNo());
                    tradeNoValue3.setText(ordInfo.getTradeNo());
                    tradeNoValue4.setText(ordInfo.getTradeNo());
                }
                else{
                    messageBox2.setText("");
                }
            }
        });

        button.setBounds(50,390,120,30);
        panel.add(button);
        return panel;
    }

    // 创建第三个标签页（发送）/ 三個目のタブ画面の宣言と設定(出金指令发送)
    private JPanel createSendingProcessTab(UserInfo userInfo, BankInfo bankInfo, OrdInfo ordInfo){

        JPanel panel = new JPanel(new GridBagLayout());

        // 共同处理 GUI/ GUI設定の共通処理
        publicProcess(userInfo,bankInfo,ordInfo,panel,balanceValue3,bankValue3,tradeNoValue3,tradeStatusValue3);

        // 消息栏/メッセージ欄
        messageBox3.setEditable(false);
        messageBox3.setLineWrap(true);
        messageBox3.setBounds(30,230,450,120);
        messageBox3.setFont(new Font("微软雅黑", Font.PLAIN, 11));
        panel.add(messageBox3);

        // 按钮/ボタン
        JButton button = new JButton("出金指令発送");
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

                if(ordInfo.getTradeStatus().equals("W2")) {
                    ordInfo.setTradeStatus("W4");
                    tradeStatusValue3.setText("W4");

                    bankInfo.setBalance(bankInfo.getBalance() + ordInfo.getWcAplAmt());
                    bankValue3.setText(String.format("%.2f", bankInfo.getBalance()) + " 元");

                    // 其他页面的修改/その他タブ画面の変更
                    tradeStatusValue1.setText("W4");
                    tradeStatusValue2.setText("W4");
                    tradeStatusValue4.setText("W4");
                    bankValue1.setText(String.format("%.2f", bankInfo.getBalance()) + " 元");
                    bankValue2.setText(String.format("%.2f", bankInfo.getBalance()) + " 元");
                    bankValue4.setText(String.format("%.2f", bankInfo.getBalance()) + " 元");

                    String msgSending = "<Trade_no>" + ordInfo.getTradeNo() + "</Trade_no>" +
                            "<Amt>" +String.format("%.2f", ordInfo.getWcAplAmt())+ "</Amt>" +
                            "<Trade_code>" + "0603" + "</Trade_code>" +
                            "<Account_name>" + "*****会社" + "</Account_name>" +
                            "<Account_no>" + "6547870" + "</Account_no>" +
                            "<Target_name>" + userInfo.getName() + "</Target_name>" +
                            "<Target_no>" + "4265802321598" + "</Target_no>" +
                            "<ID_no>" + "130503*********" + "</ID_no>";

                    messageBox3.setText("");
                    messageBox3.append("送信対象対象URL: https://cmpgdct.tarde.wsc46/servlet/APIReqServlet\n");
                    messageBox3.append("送信内容: " + msgSending + "\n");
                    messageBox3.append("返信内容: ***\n");
                    messageBox3.append("出金指令の送信が終わりました。");

                }
                else{
                    messageBox3.setText("");
                }
            }
        });

        button.setBounds(50,390,120,30);
        panel.add(button);
        return panel;
    }

    // 创建第四个标签页（查询）/ 四個目のタブ画面の宣言と設定（結果確認）
    private JPanel createResultConfirmTab(UserInfo userInfo, BankInfo bankInfo, OrdInfo ordInfo) {
        JPanel panel = new JPanel(new GridBagLayout());

        // 共同处理 GUI / GUI設定の共通処理
        publicProcess(userInfo,bankInfo,ordInfo,panel,balanceValue4,bankValue4,tradeNoValue4,tradeStatusValue4);

        // 消息栏/メッセージ欄
        messageBox4.setEditable(false);
        messageBox4.setLineWrap(true);
        messageBox4.setBounds(30,230,450,120);
        messageBox4.setFont(new Font("微软雅黑", Font.PLAIN, 11));
        panel.add(messageBox4);

        // 按钮/ボタン
        JButton button = new JButton("結果確認");
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

                if(ordInfo.getTradeStatus().equals("W4")) {
                    ordInfo.setTradeStatus("S2");
                    tradeStatusValue4.setText("S2");

                    userInfo.setBalance(userInfo.getBalance() - ordInfo.getWcAplAmt());
                    balanceValue4.setText(String.format("%.2f", userInfo.getBalance()) + " 元");

                    // 其他页面的修改/その他タブ画面の変更
                    tradeStatusValue1.setText("S2");
                    tradeStatusValue2.setText("S2");
                    tradeStatusValue3.setText("S2");
                    balanceValue1.setText(String.format("%.2f", userInfo.getBalance()) + " 元");
                    balanceValue2.setText(String.format("%.2f", userInfo.getBalance()) + " 元");
                    balanceValue3.setText(String.format("%.2f", userInfo.getBalance()) + " 元");

                    String msgSending = "<Trade_no>" + ordInfo.getTradeNo() + "</Trade_no>" +
                            "<Amt>" +String.format("%.2f", ordInfo.getWcAplAmt())+ "</Amt>" +
                            "<Trade_code>" + "0607" + "</Trade_code>" ;

                    String msgReturn = "<Trade_no>" + ordInfo.getTradeNo() + "</Trade_no>" +
                            "<Trade_code>" + "0607" + "</Trade_code>" +
                            "<Status>" + "01" + "</Status>";

                    messageBox4.setText("");
                    messageBox4.append("送信対象対象URL: https://cmpgt.query.wsc46/servlet/APIReqServlet\n");
                    messageBox4.append("送信内容: " + msgSending + "\n");
                    messageBox4.append("返信内容: " + msgReturn + "\n");
                    messageBox4.append("\n");
                    messageBox4.append("結果確認が終わりました。");
                }
                else{
                    messageBox4.setText("");
                }
            }
        });

        button.setBounds(50,390,120,30);
        panel.add(button);
        return panel;
    }

    // 共同处理 GUI/ GUI設定の共通処理
    private void publicProcess(UserInfo userInfo, BankInfo bankInfo, OrdInfo ordInfo,JPanel jPanel
    ,JLabel balanceValueJlabel, JLabel bankValueLabel, JLabel tradeNoValueLabel, JLabel tradeStatusValueLabel){
        jPanel.setLayout(null);

        // 应用标签/アプリラベル
        JLabel appLabel = new JLabel("一般口座(決済アプリ)");
        appLabel.setBounds(30, 0, 120, 25);
        appLabel.setFont(new Font("微软雅黑", Font.PLAIN, 12));
        jPanel.add(appLabel);

        // 银行标签/ラベル(銀行)
        JLabel bankLabel = new JLabel("銀行口座(ABC)");
        bankLabel.setBounds(330, 0, 120, 25);
        bankLabel.setFont(new Font("微软雅黑", Font.PLAIN, 12));
        jPanel.add(bankLabel);

        // 姓名标签/ラベル(名前)
        JLabel nameLabel = new JLabel("名前:");
        nameLabel.setBounds(10, 20, 50, 25);
        nameLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(nameLabel);

        // 姓名值显示/値(名前)
        JLabel nameValue = new JLabel(userInfo.getName());
        nameValue.setBounds(60, 20, 120, 25);
        nameValue.setFont(new Font("微软雅黑", Font.BOLD, 14));
        jPanel.add(nameValue);

        // 姓名标签(银行)/ラベル(姓名 銀行)
        JLabel bankNameLabel = new JLabel("名前:");
        bankNameLabel.setBounds(310, 20, 50, 25);
        bankNameLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(bankNameLabel);

        // 姓名值显示(銀行)/値(姓名 銀行)
        JLabel bankNameValue = new JLabel(bankInfo.getName());
        bankNameValue.setBounds(360, 20, 120, 25);
        bankNameValue.setFont(new Font("微软雅黑", Font.BOLD, 14));
        jPanel.add(bankNameValue);

        // 余额标签/ラベル(残高)
        JLabel balanceLabel = new JLabel("残高:");
        balanceLabel.setBounds(10, 40, 90, 25);
        balanceLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(balanceLabel);

        // 余额值显示/値(残高)
        balanceValueJlabel.setBounds(60, 40, 120, 25);
        balanceValueJlabel.setFont(new Font("微软雅黑", Font.BOLD, 14));
        balanceValueJlabel.setForeground(new Color(0, 100, 0)); // 绿色
        jPanel.add(balanceValueJlabel);

        // 余额标签(銀行)/ラベル(残高 銀行)
        JLabel bankBalanceLabel = new JLabel("残高:");
        bankBalanceLabel.setBounds(310, 40, 90, 25);
        bankBalanceLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(bankBalanceLabel);

        // 余额值显示(銀行)値(残高  銀行)
        bankValueLabel.setBounds(360, 40, 120, 25);
        bankValueLabel.setFont(new Font("微软雅黑", Font.BOLD, 14));
        bankValueLabel.setForeground(new Color(0, 100, 0)); // 绿色
        jPanel.add(bankValueLabel);

        // DB显示/データベース表示
        JLabel dbLineLabel = new JLabel("---------DB---------");
        dbLineLabel.setBounds(10,65,200,25);
        dbLineLabel.setFont(new Font("微软雅黑", Font.PLAIN, 16));
        jPanel.add(dbLineLabel);

        // 订单号/出金記録番号
        JLabel ordNoLabel = new JLabel("出金記録番号:");
        ordNoLabel.setBounds(10,85,120,25);
        ordNoLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(ordNoLabel);

        JLabel ordNoValue = new JLabel(ordInfo.getOrdNo());
        ordNoValue.setBounds(100,85,120,25);
        ordNoValue.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(ordNoValue);

        // 提现类型/出金タイプ
        JLabel wcTypLabel = new JLabel("出金タイプ:");
        wcTypLabel.setBounds(10,105,120,25);
        wcTypLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(wcTypLabel);

        JLabel wcTypValue = new JLabel(ordInfo.getWcType());
        wcTypValue.setBounds(100,105,120,25);
        wcTypValue.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(wcTypValue);

        // 流水号/取引番号
        JLabel tradeNoLabel = new JLabel("取引番号:");
        tradeNoLabel.setBounds(10,125,120,25);
        tradeNoLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(tradeNoLabel);

        tradeNoValueLabel.setBounds(100,125,160,25);
        tradeNoValueLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(tradeNoValueLabel);

        // 提现金额/出金金額
        JLabel wcAplAmtLabel = new JLabel("出金金額:");
        wcAplAmtLabel.setBounds(10,145,120,25);
        wcAplAmtLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(wcAplAmtLabel);

        JLabel wcAplAmtValue = new JLabel(String.format("%.2f", ordInfo.getWcAplAmt()));
        wcAplAmtValue.setBounds(100,145,120,25);
        wcAplAmtValue.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(wcAplAmtValue);

        // 目标银行/出金先銀行
        JLabel CapCorgLabel = new JLabel("出金先銀行:");
        CapCorgLabel.setBounds(10,165,120,25);
        CapCorgLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(CapCorgLabel);

        JLabel CapCorgValue = new JLabel(ordInfo.getCapCorg());
        CapCorgValue.setBounds(100,165,120,25);
        CapCorgValue.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(CapCorgValue);

        // 提现银行/出金元銀行(出金APIが使われた銀行)
        JLabel rutCorgLabel = new JLabel("出金元銀行:");
        rutCorgLabel.setBounds(10,185,120,25);
        rutCorgLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(rutCorgLabel);

        JLabel rutCorgValue = new JLabel(ordInfo.getRutCorg());
        rutCorgValue.setBounds(100,185,120,25);
        rutCorgValue.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(rutCorgValue);

        // 订单状态/出金状態
        JLabel tradeStatusLabel = new JLabel("出金状態:");
        tradeStatusLabel.setBounds(10,205,120,25);
        tradeStatusLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(tradeStatusLabel);

        tradeStatusValueLabel.setBounds(100,205,120,25);
        tradeStatusValueLabel.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        jPanel.add(tradeStatusValueLabel);
    }

    // 定义全局变量/グローバル変数の初期化
    private void globalVarProcess(OrdInfo ordInfo, UserInfo userInfo, BankInfo bankInfo){
        tradeStatusValue1 = new JLabel(ordInfo.getTradeStatus());
        tradeStatusValue2 = new JLabel(ordInfo.getTradeStatus());
        tradeStatusValue3 = new JLabel(ordInfo.getTradeStatus());
        tradeStatusValue4 = new JLabel(ordInfo.getTradeStatus());

        balanceValue1 = new JLabel(String.format("%.2f", userInfo.getBalance()) + " 元");
        balanceValue2 = new JLabel(String.format("%.2f", userInfo.getBalance()) + " 元");
        balanceValue3 = new JLabel(String.format("%.2f", userInfo.getBalance()) + " 元");
        balanceValue4 = new JLabel(String.format("%.2f", userInfo.getBalance()) + " 元");

        bankValue1 = new JLabel(String.format("%.2f", bankInfo.getBalance()) + " 元");
        bankValue2 = new JLabel(String.format("%.2f", bankInfo.getBalance()) + " 元");
        bankValue3 = new JLabel(String.format("%.2f", bankInfo.getBalance()) + " 元");
        bankValue4 = new JLabel(String.format("%.2f", bankInfo.getBalance()) + " 元");

        tradeNoValue1 = new JLabel("");
        tradeNoValue2 = new JLabel("");
        tradeNoValue3 = new JLabel("");
        tradeNoValue4 = new JLabel("");

        messageBox1 = new JTextArea();
        messageBox2 = new JTextArea();
        messageBox3 = new JTextArea();
        messageBox4 = new JTextArea();
    }

    // メイン関数
    public static void main(String[] args) {
        // 使用 SwingUtilities.invokeLater 确保 GUI 创建在事件分派线程中
        SwingUtilities.invokeLater(() -> {
            try {
                // 设置系统外观
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            } catch (Exception e) {
                e.printStackTrace();
            }
            new Withdraw_Process();
        });
    }
}