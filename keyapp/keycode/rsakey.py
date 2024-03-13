from Crypto.PublicKey import RSA
def generate_rsa_keypair(key_length):
    # 生成 RSA 密钥对
    key = RSA.generate(key_length, e=65537)

    # 获取公钥和私钥
    public_key = key.publickey().export_key().decode("utf-8")
    private_key = key.export_key().decode("utf-8")

    return public_key, private_key

def rsakey(key_length):
    # 生成密钥对
    public_key, private_key = generate_rsa_keypair(key_length)

    return [public_key,private_key]
