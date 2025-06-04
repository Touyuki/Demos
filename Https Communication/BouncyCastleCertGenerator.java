import org.bouncycastle.asn1.x500.X500Name;
import org.bouncycastle.cert.X509v3CertificateBuilder;
import org.bouncycastle.cert.jcajce.JcaX509CertificateConverter;
import org.bouncycastle.cert.jcajce.JcaX509v3CertificateBuilder;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.operator.ContentSigner;
import org.bouncycastle.operator.jcajce.JcaContentSignerBuilder;
import org.bouncycastle.util.io.pem.PemObject;
import org.bouncycastle.util.io.pem.PemWriter;

import java.io.*;
import java.math.BigInteger;
import java.security.*;
import java.security.cert.X509Certificate;
import java.util.Date;

public class BouncyCastleCertGenerator {

    static {
        Security.addProvider(new BouncyCastleProvider());
    }

    public static void main(String[] args) throws Exception {
        // 1. 生成RSA密钥对/RSA暗号鍵のペアを生成
        KeyPair keyPair = generateRSAKeyPair();

        // 2. 生成自签名证书/ディジタル証明書を生成
        X509Certificate certificate = generateSelfSignedCert(keyPair);

        // 3. 保存为PEM格式文件/ファイルに保存
        savePemFile("certificate.crt", "CERTIFICATE", certificate.getEncoded());
        savePemFile("private_receiver.key", "RSA PRIVATE KEY", keyPair.getPrivate().getEncoded());
        savePemFile("public_receiver.key","RSA PUBLIC KEY", keyPair.getPublic().getEncoded());

        // 4. 生成PKCS12密钥库/.p12ファイルを生成
        generatePKCS12KeyStore("keystore.p12", "password", keyPair, certificate);

        System.out.println("SSLディジタル証明書の生成が終わりました！");
        System.out.println("SSLディジタル証明書: certificate.crt");
        System.out.println("秘密鍵ファイル: private_receiver.key");
        System.out.println("公開鍵ファイル: public_receiver.key");
        System.out.println("PKCS12ファイル: keystore.p12 (パスワード: password)");
    }

    /**
     * 生成RSA密钥对/ RSA暗号鍵を生成
     */
    public static KeyPair generateRSAKeyPair() throws NoSuchAlgorithmException {
        KeyPairGenerator keyPairGen = KeyPairGenerator.getInstance("RSA");
        keyPairGen.initialize(2048, new SecureRandom());
        return keyPairGen.generateKeyPair();
    }

    /**
     * 生成自签名证书/SSLディジタル証明書を生成
     */
    public static X509Certificate generateSelfSignedCert(KeyPair keyPair) throws Exception {
        // 设置证书有效期（2年）/証明書有効期限を設定
        long now = System.currentTimeMillis();
        Date notBefore = new Date(now - 24 * 60 * 60 * 1000);
        Date notAfter = new Date(now + 730L * 24 * 60 * 60 * 1000); // 2年

        // 证书主题信息/証明書情報を設定
        X500Name subject = new X500Name("CN=localhost, OU=IT, O=MyCompany, L=Beijing, ST=Beijing, C=CN");

        // 构建证书/新規作成
        X509v3CertificateBuilder certBuilder = new JcaX509v3CertificateBuilder(
                subject,                          // 颁发者（自签名所以与subject相同）
                BigInteger.valueOf(now),          // 证书序列号
                notBefore,                       // 生效日期
                notAfter,                        // 过期日期
                subject,                         // 主题
                keyPair.getPublic()               // 公钥
        );

        // 使用SHA256WithRSA算法签名/アルゴリズムを指定
        ContentSigner signer = new JcaContentSignerBuilder("SHA256WithRSA").setProvider("BC").build(keyPair.getPrivate());

        // 生成X.509证书/X.509証明書を生成
        return new JcaX509CertificateConverter()
                .setProvider("BC")
                .getCertificate(certBuilder.build(signer));
    }

    /**
     * 保存为PEM格式文件/ファイルに保存する
     */
    public static void savePemFile(String filename, String type, byte[] content) throws IOException {
        PemObject pemObject = new PemObject(type, content);
        try (PemWriter pemWriter = new PemWriter(new FileWriter(filename))) {
            pemWriter.writeObject(pemObject);
        }
    }

    /**
     * 生成PKCS12密钥库/P12ファイル(秘密鍵+証明書)を生成
     */
    public static void generatePKCS12KeyStore(String filename, String password,
                                              KeyPair keyPair, X509Certificate cert) throws Exception {
        KeyStore pkcs12 = KeyStore.getInstance("PKCS12", "BC");
        pkcs12.load(null, null);
        pkcs12.setKeyEntry(
                "mykey",                         // 别名/別名
                keyPair.getPrivate(),             // 私钥/秘密鍵
                password.toCharArray(),           // 密码/パスワード
                new java.security.cert.Certificate[]{cert}  // 证书链/証明書
        );

        try (FileOutputStream fos = new FileOutputStream(filename)) {
            pkcs12.store(fos, password.toCharArray());
        }
    }
}