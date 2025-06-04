import com.sun.net.httpserver.HttpsServer;
import com.sun.net.httpserver.HttpsConfigurator;
import com.sun.net.httpserver.HttpsParameters;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import org.json.JSONObject;

import javax.net.ssl.*;
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.security.*;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

public class WorkingHttpsServer {

    // 通信端口/通信ポート
    private static final int PORT = 8443;

    // P12格式的证书文件/.p12証明書ファイル
    private static final String KEYSTORE_PATH = "C:\\Users\\xiaos\\IdeaProjects\\MessageSender\\src\\main\\java\\Keys\\keystore.p12";
    // P12文件密码/パスワード
    private static final String KEYSTORE_PASSWORD = "password";

    // 公钥(信息发送方)/公开鍵(送信側)
    private static final String PUBLIC_KEY_SENDER = "C:\\Users\\xiaos\\IdeaProjects\\MessageSender\\src\\main\\java\\Keys\\public_sender1.key";


    // 添加验签相关方法/電子署名検証
    private static boolean verifySignature(String data, String signature, PublicKey publicKey) throws Exception {
        Signature sig = Signature.getInstance("SHA256withRSA");
        sig.initVerify(publicKey);
        sig.update(data.getBytes(StandardCharsets.UTF_8));
        byte[] signatureBytes = Base64.getDecoder().decode(signature);
        return sig.verify(signatureBytes);
    }

    // 加载公钥/BASE64文字列から公開鍵に変換
    public static PublicKey loadPublicKey(String base64PublicKey) throws Exception {
        byte[] keyBytes = Base64.getDecoder().decode(base64PublicKey);
        X509EncodedKeySpec spec = new X509EncodedKeySpec(keyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        return keyFactory.generatePublic(spec);
    }

    // 读取密钥文件/ファイルから暗号鍵の文字列を読み込む
    public static String loadKeyFromFile(String filename) throws IOException {
        return new String(Files.readAllBytes(Paths.get(filename)));
    }

    public static void main(String[] args) throws Exception {
        // 1. 创建SSL上下文/SSL環境を設定
        SSLContext sslContext = createSSLContext();

        // 2. 创建HTTPS服务器/HTTPSサーバーを作る
        HttpsServer server = HttpsServer.create(new InetSocketAddress(PORT), 0);
        server.setHttpsConfigurator(new HttpsConfigurator(sslContext) {
            public void configure(HttpsParameters params) {
                try {
                    // 初始化SSL上下文/SSL環境を初期化
                    SSLContext context = getSSLContext();
                    SSLEngine engine = context.createSSLEngine();
                    params.setNeedClientAuth(false);
                    params.setCipherSuites(engine.getEnabledCipherSuites());
                    params.setProtocols(engine.getEnabledProtocols());
                    params.setSSLParameters(context.getSupportedSSLParameters());
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
            }
        });

        // 3. 创建处理程序/処理コード
        server.createContext("/api", new HttpHandler() {

            @Override
            public void handle(HttpExchange exchange) throws IOException {
                try (InputStream is = exchange.getRequestBody();
                     OutputStream os = exchange.getResponseBody()) {

                    // 1. 读取请求/送信されたデータを読み込む
                    String requestBody = new String(is.readAllBytes(), StandardCharsets.UTF_8);
                    JSONObject requestJson = new JSONObject(requestBody);
                    String receivedData = requestJson.getString("data");
                    String receivedSignature = requestJson.getString("signature");

                    System.out.println("データが送信された: " + receivedData);
                    System.out.println("電子署名が送信された: " + receivedSignature);

                    // 2. 加载公钥并验证签名/電子署名を検証
                    PublicKey publicKey = loadPublicKey(loadKeyFromFile(PUBLIC_KEY_SENDER));
                    boolean isValid = verifySignature(receivedData, receivedSignature, publicKey);

                    // 3. 根据验证结果处理/検証結果による処理
                    String response;
                    if (isValid) {
                        System.out.println("電子署名の検証が出来ました");
                        response = processRequest();
                        exchange.sendResponseHeaders(200, response.length());
                    } else {
                        System.out.println("電子署名の検証が失敗しました");
                        response = "{\"status\":\"error\",\"message\":\"電子署名検証失敗\"}";
                        exchange.sendResponseHeaders(403, response.length());
                    }

                    // 4. 设置响应头/返信設定
                    exchange.getResponseHeaders().set("Content-Type", "application/json");

                    // 5. 发送响应/返信
                    os.write(response.getBytes());
                } catch (Exception e) {
                    e.printStackTrace();
                    String error = "{\"status\":\"error\",\"message\":\"サーバー内部エラー\"}";
                    exchange.sendResponseHeaders(500, error.length());
                    exchange.getResponseBody().write(error.getBytes());
                }
            }
        });

        // 4. 启动服务器/サーバーを起動
        server.setExecutor(null);
        server.start();
        System.out.println("サーバーが起動されました: https://localhost:" + PORT + "/api");
    }

    // 创建SSL上下文/SSL環境を設定
    private static SSLContext createSSLContext() throws Exception {
        // 加载密钥库/.p12ファイルを読み込む
        KeyStore keyStore = KeyStore.getInstance("PKCS12");
        try (InputStream is = new FileInputStream(KEYSTORE_PATH)) {
            keyStore.load(is, KEYSTORE_PASSWORD.toCharArray());
        }

        // 初始化KeyManagerFactory/KeyManagerFactoryを初期化
        KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
        kmf.init(keyStore, KEYSTORE_PASSWORD.toCharArray());

        // 创建SSLContext/SSL環境を作成
        SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(kmf.getKeyManagers(), null, null);

        return sslContext;
    }

    // 处理请求并生成响应/返信処理
    private static String processRequest() {
        String response_Str = "<Trade_no>620418234561</Trade_no>" +
                "<Trade_code>0603</Trade_code>" +
                "<Status>01</Status>"+
                "<Amt>20.00</Amt>";

        return String.format("{\"status\":\"success\", \"response_Str\":\"%s\", \"timestamp\":%d}",
                response_Str, System.currentTimeMillis());
    }
}