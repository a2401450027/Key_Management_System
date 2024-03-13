from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def generate_des_key(key_length):
    # DES 密钥长度为 8 字节
    des_key_size = 8

    # 如果输入的长度小于 DES 密钥长度，使用 PKCS7 填充
    if key_length < des_key_size:
        padded_key = pad(str(key_length).encode(), des_key_size)
    else:
        padded_key = pad(str(key_length)[:des_key_size].encode(), des_key_size)

    # 使用 get_random_bytes 生成随机的初始化向量
    iv = get_random_bytes(8)

    # 创建 DES 密钥对象
    des_cipher = DES.new(padded_key, DES.MODE_CBC, iv)

    # 返回包含密钥和初始化向量的元组
    return str(padded_key), str(iv)


def deskey(length):


    # 生成 DES 密钥
    key, iv = generate_des_key(length)
    return [key,iv]
