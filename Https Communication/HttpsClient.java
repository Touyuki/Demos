import javax.net.ssl.*;
import java.io.*;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.security.*;
import java.util.Base64;
import java.security.spec.PKCS8EncodedKeySpec;
import org.json.JSONObject;
public class HttpsClient {

    // https通信URL/HTTPS通信用URL
    private static final String RECEIVER_URL = "https://localhost:8443/api";

    // P12格式的证书文件/.p12証明書ファイル
    private static final String TRUSTSTORE_PATH = "C:\\Users\\xiaos\\IdeaProjects\\MessageSender\\src\\main\\java\\Keys\\keystore.p12";
    // P12文件密码/パスワード
    private static final String TRUSTSTORE_PASSWORD = "password";

    // 私钥(信息发送方)/秘密鍵(送信側)
    private static final String PRIVATE_KEY_SENDER = "C:\\Users\\xiaos\\IdeaProjects\\MessageSender\\src\\main\\java\\Keys\\private_sender1.key";

    // 添加签名相关方法/電子署名を作成
    private static String signData(String data, PrivateKey privateKey) throws Exception {
        Signature signature = Signature.getInstance("SHA256withRSA");
        signature.initSign(privateKey);
        signature.update(data.getBytes(StandardCharsets.UTF_8));
        byte[] digitalSignature = signature.sign();
        return Base64.getEncoder().encodeToString(digitalSignature);
    }

    // 加载私钥/BASE64文字列から秘密鍵に変換
    private static PrivateKey loadPrivateKey(String base64PrivateKey) throws Exception {
        byte[] keyBytes = Base64.getDecoder().decode(base64PrivateKey);
        PKCS8EncodedKeySpec spec = new PKCS8EncodedKeySpec(keyBytes);
        KeyFactory kf = KeyFactory.getInstance("RSA");
        return kf.generatePrivate(spec);
    }

    // 读取密钥文件/ファイルから暗号鍵の文字列を読み込む
    public static String loadKeyFromFile(String filename) throws IOException {
        return new String(Files.readAllBytes(Paths.get(filename)));
    }

    public static void main(String[] args) throws Exception {

        // 1. 配置SSL上下文（信任自签名证书）/SSL環境を設定
        SSLContext sslContext = createSSLContext();

        // 2. 准备请求数据/送信データ
        String requestData = "<Trade_no>620418234561</Trade_no>" +
                "<Amt>20.00</Amt>" +
                "<Trade_code>0603</Trade_code>" +
                "<Account_name>qp*****</Account_name>" +
                "<Account_no>6547870</Account_no>" +
                "<Target_name>zws</Target_name>" +
                "<Target_no>4265802321598</Target_no>" +
                "<ID_no>130503*********</ID_no>";
        System.out.println("送信内容: " + requestData);

        // 3. 生成签名/電子署名を作る
        PrivateKey privateKey = loadPrivateKey(loadKeyFromFile(PRIVATE_KEY_SENDER));
        String signature = signData(requestData, privateKey);
        System.out.println("電子署名: " + signature);

        // 4. 创建包含数据和签名的JSON/JSON変数を作る
        JSONObject requestJson = new JSONObject();
        requestJson.put("data", requestData);
        requestJson.put("signature", signature);
        String requestBody = requestJson.toString();

        // 5. 创建HTTPS连接/HTTPS通信を作成
        URL url = new URL(RECEIVER_URL);
        HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
        connection.setSSLSocketFactory(sslContext.getSocketFactory());
        connection.setHostnameVerifier((hostname, session) -> true); // 跳过主机名验证（仅测试用）/ホスト名検証を飛ばす

        // 6. 设置请求属性/通信設定
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/json");
        connection.setDoOutput(true);

        // 5. 发送请求数据/送信
        try (OutputStream os = connection.getOutputStream()) {
            byte[] input = requestBody.getBytes(StandardCharsets.UTF_8);
            os.write(input, 0, input.length);
        }

        // 6. 读取响应状态/返信状態確認
        int responseCode = connection.getResponseCode();
        System.out.println("返信された状態コード: " + responseCode);

        // 7. 读取响应内容/返信内容を読む
        if (responseCode == HttpsURLConnection.HTTP_OK) {
            try (BufferedReader br = new BufferedReader(
                    new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                StringBuilder response = new StringBuilder();
                String responseLine;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine);
                }
                System.out.println("サーバーからの返信情報: " + response.toString());
            }
        } else {
            try (BufferedReader br = new BufferedReader(
                    new InputStreamReader(connection.getErrorStream(), StandardCharsets.UTF_8))) {
                String errorResponse = br.readLine();
                System.out.println("通信エラーが発生しました: " + errorResponse);
            }
        }
    }


    // 配置SSL上下文/SSL環境を設定
    private static SSLContext createSSLContext() throws Exception {
        // 加载信任库（包含服务器证书）/サーバーの証明書を読み込む
        KeyStore trustStore = KeyStore.getInstance("PKCS12");
        try (InputStream is = new FileInputStream(TRUSTSTORE_PATH)) {
            trustStore.load(is, TRUSTSTORE_PASSWORD.toCharArray());
        }

        // 初始化TrustManagerFactory/初期化
        TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
        tmf.init(trustStore);

        // 创建SSLContext/SSL環境作成
        SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(null, tmf.getTrustManagers(), null);

        return sslContext;
    }
}