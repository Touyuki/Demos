import java.io.IOException;
import java.security.*;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;
import java.nio.file.Files;
import java.nio.file.Paths;

public class RSAKeyPairGenerator {

    public static void main(String[] args) throws Exception {
        // 1. 生成RSA密钥对/RSA暗号鍵のペアを生成
        KeyPair keyPair = generateRSAKeyPair();

        // 2. 获取公钥和私钥/公開鍵、秘密鍵を取得
        PublicKey publicKey = keyPair.getPublic();
        PrivateKey privateKey = keyPair.getPrivate();

        // 3. 转换为Base64字符串格式（便于存储）/BASE64で文字列に変換
        String publicKeyStr = Base64.getEncoder().encodeToString(publicKey.getEncoded());
        String privateKeyStr = Base64.getEncoder().encodeToString(privateKey.getEncoded());

        System.out.println("公開鍵(Base64):");
        System.out.println(publicKeyStr);
        System.out.println("\n秘密鍵(Base64):");
        System.out.println(privateKeyStr);

//        PrivateKey privateKey = loadPrivateKey(loadKeyFromFile("C:\\Users\\xiaos\\IdeaProjects\\MessageSender\\src\\main\\java\\Keys\\private_sender1.key"));
//        PublicKey publicKey = loadPublicKey(loadKeyFromFile("C:\\Users\\xiaos\\IdeaProjects\\MessageSender\\src\\main\\java\\Keys\\public_sender1.key"));

        // 4. 测试签名和验证/署名と検証
        String originalData = "検証用データ123456";
        System.out.println("\n生データ: " + originalData);

        // 签名/電子署名
        String signature = signData(originalData, privateKey);
        System.out.println("電子署名: " + signature);

        // 验证/検証
        boolean isValid = verifySignature(originalData, signature, publicKey);
        System.out.println("検証結果: " + isValid);

        //保存为文件/ファイルに保存
//        saveKeyToFile("public_sender1.key", publicKeyStr);
//        saveKeyToFile("private_sender1.key", privateKeyStr);
    }

    /**
     * 生成RSA密钥对/RSA暗号鍵のペアを生成
     */
    public static KeyPair generateRSAKeyPair() throws NoSuchAlgorithmException {
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA");
        keyPairGenerator.initialize(2048); // 密钥长度2048位
        return keyPairGenerator.generateKeyPair();
    }

    /**
     * 使用私钥对数据进行签名/秘密鍵による電子署名を生成
     */
    public static String signData(String data, PrivateKey privateKey) throws Exception {
        Signature signature = Signature.getInstance("SHA256withRSA");
        signature.initSign(privateKey);
        signature.update(data.getBytes());
        byte[] signatureBytes = signature.sign();
        return Base64.getEncoder().encodeToString(signatureBytes);
    }

    /**
     * 使用公钥验证签名/公開鍵で署名を検証
     */
    public static boolean verifySignature(String data, String signature, PublicKey publicKey) throws Exception {
        Signature sig = Signature.getInstance("SHA256withRSA");
        sig.initVerify(publicKey);
        sig.update(data.getBytes());
        byte[] signatureBytes = Base64.getDecoder().decode(signature);
        return sig.verify(signatureBytes);
    }

    /**
     * 从Base64字符串加载公钥/BASE64文字列から公開鍵に変換
     */
    public static PublicKey loadPublicKey(String base64PublicKey) throws Exception {
        byte[] keyBytes = Base64.getDecoder().decode(base64PublicKey);
        X509EncodedKeySpec spec = new X509EncodedKeySpec(keyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        return keyFactory.generatePublic(spec);
    }

    /**
     * 从Base64字符串加载私钥/BASE64文字列から秘密鍵に変換
     */
    public static PrivateKey loadPrivateKey(String base64PrivateKey) throws Exception {
        byte[] keyBytes = Base64.getDecoder().decode(base64PrivateKey);
        PKCS8EncodedKeySpec spec = new PKCS8EncodedKeySpec(keyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        return keyFactory.generatePrivate(spec);
    }

    // 保存为文件/暗号鍵をファイルに保存する
    public static void saveKeyToFile(String filename, String key) throws IOException {
        Files.write(Paths.get(filename), key.getBytes());
    }

    // 从文件中读取密钥字符串/ファイルから暗号鍵の文字列を読み込む
    public static String loadKeyFromFile(String filename) throws IOException {
        return new String(Files.readAllBytes(Paths.get(filename)));
    }
}