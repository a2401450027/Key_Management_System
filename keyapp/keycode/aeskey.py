from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def generate_aes_key_and_iv(key_length):
    # 生成随机的 key
    if key_length // 8 <=8:
        length = key_length
    else: length = 8
    key = get_random_bytes(length)

    # 生成随机的初始向量
    iv = get_random_bytes(AES.block_size)

    # 补齐至指定位数
    while len(key) < AES.block_size:
        key += get_random_bytes(1)

    return key, iv

def aeskey(key_length):
    # 生成 AES 密钥和初始向量
    aes_key, iv = generate_aes_key_and_iv(key_length)
    return [base64.b64encode(aes_key).decode('utf-8'), base64.b64encode(iv).decode('utf-8')]
