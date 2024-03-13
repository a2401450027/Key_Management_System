import secrets
import string

def generate_strong_password(length):
    # 定义密码字符集，包括大小写字母、数字和特殊字符
    characters = string.ascii_letters + string.digits + string.punctuation

    # 生成密码
    password = ''.join(secrets.choice(characters) for _ in range(length))

    return password

def selfkey(length):

    # 生成强密码
    strong_password = generate_strong_password(length)

    return strong_password
